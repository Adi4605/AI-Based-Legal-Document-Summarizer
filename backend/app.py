from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import re

from extractor import extract_text
from classifier import classify_document
from summarizer import generate_summary

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def format_bullets(items):
    if not items:
        return "Not clearly specified in the document"
    return "\n".join(f"• {item}" for item in items)

#Party Extraction
def extract_parties(text):
    """
    Extract real human names, ignore roles and noise.
    """
    pattern = r"Mr\.?\s+[A-Z][a-zA-Z]+\s+[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?"
    matches = re.findall(pattern, text)

    parties = set()
    for m in matches:
        if len(m.split()) >= 2:
            parties.add(m.strip())

    return list(parties)

#Data Extraction
def extract_dates(text):
    """
    Extract only real calendar dates.
    """
    patterns = [
        r"\b\d{2}/\d{2}/\d{4}\b",
        r"\b\d{1,2}\s+[A-Z][a-z]+\s+\d{4}\b"
    ]

    dates = set()
    for p in patterns:
        dates.update(re.findall(p, text))

    return list(dates)

# Clause Parser
def extract_clauses(text):
    """
    Extract numbered legal clauses as full units.
    """
    pattern = re.compile(r"\n\s*(\d+\))")
    parts = pattern.split(text)

    clauses = []
    for i in range(1, len(parts), 2):
        clause_no = parts[i]
        clause_body = parts[i + 1]

        cleaned = " ".join(clause_body.split())
        if len(cleaned) > 50:
            clauses.append(f"{clause_no} {cleaned}")

    return clauses

#Conditions
def extract_conditions(text):
    clauses = extract_clauses(text)

    conditions = []
    for c in clauses:
        c_lower = c.lower()

        #Party identification clauses
        if any(k in c_lower for k in ["name:", "age", "pan", "aadhaar", "residing at"]):
            continue

        #Penalty clauses
        if any(k in c_lower for k in ["terminate", "termination", "cancel", "breach", "damages"]):
            continue

        #Real conditions
        if any(k in c_lower for k in ["period", "license", "fee", "use", "premises", "rent", "compensation"]):
            conditions.append(c)

    return conditions[:5]

def extract_penalties(text):
    clauses = extract_clauses(text)

    penalties = []
    for c in clauses:
        if any(
            k in c.lower()
            for k in ["terminate", "termination", "cancel", "breach", "damages", "revoke", "double"]
        ):
            penalties.append(c)

    return penalties[:4]

def extract_dates_with_importance(text):
    import re
    important_dates = []
    sentences = re.split(r'(?<=[.;])\s+', text)
    date_pattern = r"\b\d{2}/\d{2}/\d{4}\b"
    for sentence in sentences:
        dates = re.findall(date_pattern, sentence)
        if len(dates) >= 2:
            important_dates.append(
                f"{dates[0]} – Commencement / start date of the agreement"
            )
            important_dates.append(
                f"{dates[1]} – Expiry / end date of the agreement"
            )
            continue
        if len(dates) == 1:
            d = dates[0]
            s = sentence.lower()
            if any(k in s for k in ["commenc", "start", "effective from"]):
                reason = "Commencement / start date of the agreement"
            elif any(k in s for k in ["ending", "expire", "expiry", "termination"]):
                reason = "Expiry / end date of the agreement"
            else:
                reason = "Important date mentioned in the document"
            important_dates.append(f"{d} – {reason}")

    # Remove duplicates
    seen = set()
    final = []
    for d in important_dates:
        if d not in seen:
            seen.add(d)
            final.append(d)

    return final

from transformers import pipeline

legal_classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=-1  # CPU
)

def is_legal_document_ml(text):
    """
    AI-based legal / non-legal document classifier.
    """
    labels = ["legal document", "non-legal document"]
    snippet = text[:1200]
    result = legal_classifier(
        snippet,
        candidate_labels=labels
    )
    label = result["labels"][0]
    confidence = result["scores"][0]
    is_legal = (label == "legal document") and confidence >= 0.6
    return is_legal, confidence

#API
@app.post("/summarize")
async def summarize(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    text = extract_text(file_path)
    if not text.strip():
        return {"summary": "Unable to extract text from document"}
    doc_type = classify_document(text)
    parties = extract_parties(text)
    dates=extract_dates_with_importance(text)
    conditions = extract_conditions(text)
    penalties = extract_penalties(text)
    is_legal, confidence = is_legal_document_ml(text)
    if not is_legal:
        return {
            "summary": (
                "This document is classified as a NON-LEGAL document.\n\n"
                f"AI confidence score: {confidence:.2f}\n\n"
                "The system only summarizes legal documents such as contracts, "
                "agreements, notices, or court orders."
            )
        }
    summary = generate_summary(text)
    final_output = f"""
$$ DOCUMENT TYPE
{doc_type}

$$ PARTIES INVOLVED
{format_bullets(parties)}

$$ CONDITIONS / KEY CLAUSES
{format_bullets(conditions)}

$$ OBLIGATIONS & PENALTIES
{format_bullets(penalties)}

$$ IMPORTANT DATES
{format_bullets(dates)}

$$ SUMMARY (LAWYER EXPLANATION)
{summary}

$$ OVERALL LEGAL INTERPRETATION
This document creates legally enforceable rights and obligations between the listed parties.
Non-compliance with the stated conditions may result in termination, financial liability, or other legal consequences as described above.
"""
    return {"summary": final_output}

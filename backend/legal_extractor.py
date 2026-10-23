import re
import spacy
from clause_parser import extract_clauses

nlp = spacy.load("en_core_web_sm")

def extract_parties(text):
    names = set()

    pattern = r"Mr\.?\s+[A-Z][a-zA-Z]+\s+[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?"
    matches = re.findall(pattern, text)

    for m in matches:
        if len(m.split()) >= 2:
            names.add(m.strip())

    return list(names)

def extract_dates_with_importance(text):
    """
    Extract dates and infer their legal importance from context.
    """
    date_pattern = r"\b\d{2}/\d{2}/\d{4}\b"
    matches = list(re.finditer(date_pattern, text))

    important_dates = []

    for m in matches:
        date = m.group()
        start = max(0, m.start() - 120)
        end = min(len(text), m.end() + 120)
        context = text[start:end].lower()

        # Infer importance
        if any(k in context for k in ["commencing", "commence", "effective from", "starting from"]):
            reason = "Commencement / start date of the agreement"

        elif any(k in context for k in ["ending on", "expire", "expiry", "termination"]):
            reason = "Expiry / end date of the agreement"

        elif any(k in context for k in ["notice", "notice period"]):
            reason = "Notice period related date"

        elif any(k in context for k in ["payment", "fee", "rent"]):
            reason = "Payment-related due date"

        else:
            reason = "Significant date mentioned in the document"

        important_dates.append(f"{date} – {reason}")

    return list(dict.fromkeys(important_dates))  # remove duplicates

def extract_conditions(text):
    clauses = extract_clauses(text)

    condition_clauses = []
    for c in clauses:
        if not any(k in c.lower() for k in ["terminate", "termination", "cancel", "breach", "penalty", "damages"]):
            condition_clauses.append(c)

    return condition_clauses[:5]

def extract_penalties(text):
    clauses = extract_clauses(text)

    penalty_clauses = []
    for c in clauses:
        if any(k in c.lower() for k in ["terminate", "termination", "cancel", "breach", "damages", "revoke"]):
            penalty_clauses.append(c)

    return penalty_clauses[:4]
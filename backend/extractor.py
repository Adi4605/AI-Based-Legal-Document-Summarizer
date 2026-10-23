import fitz
import docx

def extract_text(path):
    if path.endswith(".pdf"):
        doc = fitz.open(path)
        return " ".join(page.get_text() for page in doc)

    if path.endswith(".docx"):
        d = docx.Document(path)
        return " ".join(p.text for p in d.paragraphs)

    if path.endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    return ""

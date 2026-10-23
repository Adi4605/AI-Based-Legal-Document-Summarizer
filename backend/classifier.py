def classify_document(text):
    text = text.lower()

    if "agreement" in text:
        return "Contract / Agreement"
    if "lease" in text:
        return "Lease Deed"
    if "court" in text or "judgment" in text:
        return "Court Order / Judgment"
    if "will" in text:
        return "Will / Testament"
    if "notice" in text:
        return "Legal Notice"

    return "General Legal Document"

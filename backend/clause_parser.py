import re

def extract_clauses(text):
    """
    Extract numbered legal clauses as full units.
    """
    pattern = re.compile(r"\n\s*(\d+\))")
    splits = pattern.split(text)

    clauses = []
    for i in range(1, len(splits), 2):
        clause_number = splits[i]
        clause_text = splits[i + 1].strip()

        cleaned = " ".join(clause_text.split())
        if len(cleaned) > 50:
            clauses.append(f"{clause_number} {cleaned}")

    return clauses

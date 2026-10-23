from transformers import pipeline

print("-----------Loading T5 model...")

summarizer = pipeline(
    "summarization",
    model="t5-small",
    device=-1
)

print("$$$$ Model loaded")

def generate_summary(text):
    text = text[:1500]

    prompt = (
        "Explain this legal document in simple terms as a lawyer would explain to a client. "
        "Focus on purpose, rights, obligations, and risks:\n\n" + text
    )

    output = summarizer(
        prompt,
        max_new_tokens=140,
        do_sample=False
    )

    return output[0]["summary_text"]
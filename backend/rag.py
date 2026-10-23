from sentence_transformers import SentenceTransformer
import faiss
import os

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    cache_folder="./models"
)

def build_vector_store(text):
    chunks = [text[i:i+800] for i in range(0, len(text), 800)]
    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(embeddings)
    return chunks, index, embeddings

def retrieve(chunks, index, query):
    q_emb = model.encode([query])
    _, idx = index.search(q_emb, 3)
    return " ".join([chunks[i] for i in idx[0]])

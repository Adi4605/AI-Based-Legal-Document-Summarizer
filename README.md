# AI-Based Legal Document Summarizer

A web application that reads a legal document and produces a short summary along with its key details. It uses NLP and Hugging Face Transformer models, with a Python backend and a simple web interface.

## Features

- **Upload a legal document** through the web interface and get a summary back
- **Document classification:** identifies the type of document
- **Key detail extraction:** pulls out parties, obligations, conditions, penalties, and dates
- **Clause parsing:** breaks the document into clauses for easier processing

## Tech Stack

- **Language:** Python, JavaScript
- **Backend:** FastAPI
- **NLP / ML:** Hugging Face Transformers
- **Frontend:** HTML, CSS, JavaScript

## Project Structure

```
Legal Document Summarizer 2/
├── backend/
│   ├── app.py              # API server (entry point)
│   ├── classifier.py       # Document type classification
│   ├── summarizer.py       # Summary generation
│   ├── extractor.py        # Key detail extraction
│   ├── legal_extractor.py  # Legal-specific extraction
│   ├── clause_parser.py    # Splits the document into clauses
│   ├── rag.py              # Retrieval support
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Web page
│   ├── script.js           # Upload and display logic
│   └── style.css           # Styling
└── README.md
```

## Setup and Run

1. **Clone the repository**
   ```
   git clone <your-repo-url>
   cd "Legal Document Summarizer 2"
   ```

2. **Create and activate a virtual environment**
   ```
   cd backend
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Start the backend**
   ```
   uvicorn app:app --reload
   ```

5. **Open the frontend:** open `frontend/index.html` in your browser, upload a document, and view the summary.

## Models

Model files are not included in this repository because of their size. The Hugging Face models are downloaded automatically the first time the app runs, so an internet connection is needed on the first run.

## Notes

- This is a student project built for learning and is not a substitute for professional legal advice.
- Sample documents are not included. Use your own non-sensitive text or PDF files to test it.

## Author

Aditya Tungar
[LinkedIn](https://linkedin.com/in/aditya-tungar) | [GitHub](https://github.com/Adi4605)

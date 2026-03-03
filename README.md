# Questionnaire AI – Structured Questionnaire Answering Tool

A web-based AI tool to **automatically answer structured questionnaires** using a **Retrieval-Augmented Generation (RAG) pipeline** with references. Users can upload questionnaires and supporting documents, generate AI answers grounded in the references, review and edit them, and export the results as a Word document.

---

## 🛠 Features

- **User authentication** with username/password.
- **Upload questionnaires (PDF)** and reference documents (PDF/TXT/MD).
- **Automatic question detection** from uploaded PDFs.
- **RAG pipeline for AI answers**:
  - Uses context from uploaded reference files.
  - Returns citations for generated answers.
  - Fallback: “Not found in references” if information is missing.
- **Review & Edit answers** before export.
- **Export answers** as a Word document (`.docx`) preserving structure and citations.
- **Persistent storage** using SQLite database (`save_session` and `save_answers`).
- **Optional LLM providers**:
  - OpenAI (`ChatOpenAI`) – requires API key and billing.
  - Groq (`ChatGroq`) – free, fast, zero-cost alternative.
  - HuggingFace embeddings for vector store (free & local).

---
```
## 📂 Project Structure
questionnaire-ai/
│
├── backend/
│ ├── rag.py # RAG pipeline + vector store
│ ├── database.py # SQLite database handling
│ ├── auth.py # Authentication using Streamlit-authenticator
│ ├── export_utils.py # Export to .docx
│ ├── models.py # Question & Answer data models
│ └── requirements.txt # Backend dependencies
│
├── frontend/
│ └── streamlit_app.py # Main Streamlit app
│
└── docs/
├── sample_questionnaire.pdf
├── sample_questionnaire.xlsx
└── reference_docs/
├── security_policy.pdf
├── compliance_overview.pdf
├── infrastructure_overview.pdf
├── access_control_policy.pdf
└── incident_response_plan.pdf
```

---

## ⚡ Setup & Deployment Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/jyothir-369/questionnaire-ai.git
cd questionnaire-ai
2️⃣ Install Python Dependencies
pip install -r backend/requirements.txt
pip install streamlit sentence-transformers PyMuPDF faiss-cpu
pip install langchain langchain-community
3️⃣ Optional: Install Groq (Free LLM)
pip install langchain-groq
$env:GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
4️⃣ Optional: Use OpenAI LLM
$env:OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
5️⃣ Run the Streamlit App
streamlit run frontend/streamlit_app.py

Open your browser at http://localhost:8501/
 and log in:

Username: admin

Password: test123 🔑

🖥 Deployment Options
Option 1: Streamlit Community Cloud (Recommended)

Push your repository to GitHub.

Go to Streamlit Cloud

Click New App → Connect GitHub repository

Select branch and file: frontend/streamlit_app.py

Add API keys in Settings → Secrets

Deploy and get your live URL 🌐

Option 2: Render

Create a new Web Service on Render

Connect your GitHub repository

Set Start Command:

streamlit run frontend/streamlit_app.py --server.port $PORT

Add environment variables for API keys

Deploy and access via the provided URL

Option 3: Local / VPS

Install dependencies on the server

Run:

streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0

Access via: http://<server-ip>:8501/

🧠 How It Works
1️⃣ Upload Questionnaire + Reference Docs

PDF questions are parsed automatically

Reference docs converted to text and split into chunks

2️⃣ Vector Store Creation

Embeddings are created using HuggingFace Embeddings

Stored in FAISS for fast similarity search

3️⃣ Answer Generation (RAG)

Similar chunks retrieved from FAISS

Passed to LLM (Groq / OpenAI) with context

Citations extracted from retrieved documents

If no info → returns “Not found in references.”

4️⃣ Review & Edit

Answers shown in Review tab

Users can edit before export

5️⃣ Export

Answers saved as .docx with citations

✅ Assignment Compliance
Requirement	Status
User authentication	✅ Done
Persistent database storage	✅ Done
Upload → Generate → Review → Export flow	✅ Done
AI-generated answers grounded in references	✅ Done
Citations included in output	✅ Done
“Not found in references” fallback	✅ Done
Export Word document	✅ Done
Free / optional API provider (Groq / HuggingFace)	✅ Done

⚠️ Only remaining issue is OpenAI quota if using OpenAI embeddings/LLM.

🔧 Notes

File limits: 200MB per file (PDF/TXT/MD)

Detected questions: Based on numbering or question marks

Embeddings: sentence-transformers/all-MiniLM-L6-v2

Vector store: FAISS, local and fast

Local environment: No cloud deployment needed unless you want a live demo

📦 Dependencies

Python 3.12+

streamlit

sentence-transformers

PyMuPDF

faiss-cpu

langchain

langchain-community

langchain-groq (if using Groq)

🔗 References

LangChain Documentation

FAISS

Sentence Transformers

Streamlit

👤 Author

Jyothir Raghavalu Bhogi
Email: jyothirraghavalu369@gmail.com

GitHub: jyothir-369

🚀 Quick Start for Evaluators

Run and test the app locally in 3 commands:

git clone https://github.com/jyothir-369/questionnaire-ai.git
cd questionnaire-ai
streamlit run frontend/streamlit_app.py

Open your browser at http://localhost:8501/
 and log in with admin credentials.
Username: admin | Password: test123


---

If you want, I can **also add a “Screenshots” section with the Upload → Review → Export tabs** so the README looks really polished on GitHub.  

Do you want me to do that next?
Do you want me to add that?

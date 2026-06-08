# Questionnaire AI

## Overview

Questionnaire AI is a Retrieval-Augmented Generation (RAG) platform that automates answering structured questionnaires using enterprise knowledge sources. The system enables users to upload questionnaires and supporting documents, retrieve relevant context through semantic search, generate grounded AI responses with citations, review outputs, and export completed questionnaires.

This project demonstrates practical applications of Large Language Models (LLMs), vector databases, retrieval systems, prompt orchestration, and production-ready AI workflows.

---

## Features

- AI-powered questionnaire answering using RAG architecture
- Semantic retrieval with vector embeddings and FAISS
- Citation-aware answer generation
- Automated questionnaire parsing from PDF documents
- Multi-document knowledge ingestion and retrieval
- Review and edit workflow for generated answers
- Export responses as Word documents (.docx)
- User authentication and session management
- Persistent storage using SQLite
- Support for OpenAI and Groq LLM providers

---

## Architecture

### Document Processing
- Upload questionnaires and reference documents
- Extract and preprocess text from PDF, TXT, and Markdown files
- Automatically identify and structure questionnaire items

### Retrieval Layer
- Generate embeddings using Sentence Transformers
- Store vectors in FAISS for efficient similarity search
- Retrieve relevant document chunks for each question

### Generation Layer
- Combine retrieved context with prompt templates
- Generate grounded answers using LLMs
- Return source citations alongside generated responses
- Handle missing information through fallback mechanisms

### Review & Export
- Human-in-the-loop answer validation
- Editable response workflow
- Export final questionnaire responses to DOCX format

---

## Technology Stack

### AI & Retrieval
- LangChain
- OpenAI API
- Groq API
- Sentence Transformers
- FAISS
- Retrieval-Augmented Generation (RAG)

### Backend
- Python
- SQLite
- PyMuPDF

### Frontend
- Streamlit

### DevOps & Tooling
- Git
- GitHub

---

## Project Structure

```text
questionnaire-ai/
│
├── backend/
│   ├── rag.py
│   ├── database.py
│   ├── auth.py
│   ├── export_utils.py
│   └── models.py
│
├── frontend/
│   └── streamlit_app.py
│
└── docs/
    ├── sample_questionnaire.pdf
    └── reference_documents/
```

---

## AI Workflow

1. Upload questionnaire and supporting documents.
2. Extract and preprocess document content.
3. Generate embeddings using Sentence Transformers.
4. Store embeddings in FAISS vector database.
5. Retrieve relevant context using semantic search.
6. Pass retrieved context to the LLM through a RAG pipeline.
7. Generate citation-aware answers.
8. Review and edit responses.
9. Export completed questionnaire as a DOCX document.

---

## Technical Highlights

- Built an end-to-end RAG pipeline for enterprise document question answering.
- Implemented vector search using FAISS and transformer-based embeddings.
- Designed prompt orchestration workflows for grounded answer generation.
- Integrated OpenAI and Groq LLM providers for flexible deployment.
- Developed citation-aware response generation to improve answer traceability.
- Implemented persistent session and answer storage using SQLite.
- Designed scalable document ingestion and retrieval workflows.

---

## Future Enhancements

- Multi-agent answer validation workflows
- Automated evaluation and feedback pipelines
- Hybrid search (keyword + vector retrieval)
- Support for larger document collections
- Role-based access control
- Cloud deployment with observability and monitoring

---

## Author

**Jyothir Raghavalu Bhogi**

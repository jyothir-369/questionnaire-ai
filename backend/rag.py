# backend/rag.py

import os
from pathlib import Path
from typing import List, Tuple

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# ✅ Groq LLM
from langchain_groq import ChatGroq

# ✅ Local/fallback embeddings
from langchain_community.embeddings import HuggingFaceEmbeddings


def build_vectorstore(reference_paths: List[Path]) -> FAISS:
    """
    Build a FAISS vector store from reference documents (PDF or text).
    """
    docs = []
    for path in reference_paths:
        if path.suffix.lower() == ".pdf":
            loader = PyMuPDFLoader(str(path))
        else:
            loader = TextLoader(str(path), encoding="utf-8")
        docs.extend(loader.load())

    if not docs:
        raise ValueError("No documents loaded from reference paths")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True
    )
    splits = text_splitter.split_documents(docs)

    if not splits:
        raise ValueError("No text chunks created after splitting")

    # ✅ Use HuggingFace embeddings instead of OpenAI
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(splits, embeddings)
    return vectorstore


def answer_question(question: str, vectorstore: FAISS, llm=None) -> Tuple[str, List[str]]:
    """
    Answer a question using RAG with citations.
    Returns (answer_text, list_of_citation_snippets)
    """
    if llm is None:
        # ✅ Use ChatGroq instead of OpenAI
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    # Modern LCEL chain style
    prompt_template = """You are a precise assistant answering compliance/security questionnaires.
Use **only** the provided context to answer. Be concise and factual.
If the information is not in the context, respond exactly with: "Not found in references."

Context:
{context}

Question: {question}

Answer:"""

    prompt = ChatPromptTemplate.from_template(prompt_template)

    rag_chain = (
        {"context": retriever | (lambda docs: "\n\n".join(doc.page_content for doc in docs)),
         "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    try:
        answer = rag_chain.invoke(question)

        # Retrieve documents again for citations
        retrieved_docs = retriever.invoke(question)

        # Simple citation format
        citations = []
        for i, doc in enumerate(retrieved_docs, 1):
            snippet = doc.page_content[:180].replace("\n", " ").strip()
            citations.append(f"[{i}] {snippet}...")

        if "Not found in references" in answer:
            citations = []

        return answer.strip(), citations

    except Exception as e:
        return f"Error generating answer: {str(e)}", []
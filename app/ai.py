import os
import httpx
from typing import List
from . import models, schemas

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")

def format_students(students: List[models.Student]) -> str:
    if not students:
        return "No student records found."
    lines = []
    for s in students:
        lines.append(
            f"ID: {s.student_id}, Name: {s.name}, DOB: {s.date_of_birth}, "
            f"Email: {s.email or 'N/A'}, Phone: {s.phone or 'N/A'}, "
            f"Course: {s.course or 'N/A'}, Address: {s.address or 'N/A'}, "
            f"Enrollment: {s.enrollment_date or 'N/A'}"
        )
    return "\n".join(lines)

def ask_ollama(question: str, students: List[models.Student]) -> schemas.AskResponse:
    context = format_students(students)
    prompt = f"""You are a helpful assistant for a student database. Answer the user's question based ONLY on the records provided below. If the answer is not in the records, say you don't know. Do not make up information. Do not execute SQL.

Records:
{context}

Question: {question}
Answer:"""
    try:
        response = httpx.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.2}
            },
            timeout=60.0
        )
        response.raise_for_status()
        data = response.json()
        answer = data.get("response", "").strip()
        return schemas.AskResponse(answer=answer, model=OLLAMA_MODEL, records_used=len(students))
    except httpx.HTTPError as e:
        return schemas.AskResponse(answer=f"Could not reach Ollama: {e}", model=OLLAMA_MODEL, records_used=0)
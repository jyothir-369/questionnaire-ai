# backend/models.py

from pydantic import BaseModel, Field
from typing import List, Optional

class Question(BaseModel):
    number: int
    text: str

class Answer(BaseModel):
    question: Question
    text: str
    citations: List[str] = Field(default_factory=list)
    not_found: bool = False

class QuestionnaireSession(BaseModel):
    id: Optional[int] = None
    filename: str
    questions: List[Question] = Field(default_factory=list)
    answers: List[Answer] = Field(default_factory=list)
    created_at: Optional[str] = None
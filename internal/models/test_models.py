from pydantic import BaseModel
from typing import List, Optional

class CreateTestRequest(BaseModel):
    title: str
    description: Optional[str] = None
    duration_minutes: int
    random_questions_count: int

class TestResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    duration_minutes: int
    is_published: bool
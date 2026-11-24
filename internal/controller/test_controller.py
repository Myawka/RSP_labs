from fastapi import APIRouter
from internal.models.test_models import CreateTestRequest, TestResponse

router = APIRouter(prefix="/api/v1/tests", tags=["Tests"])

@router.get("", response_model=list[TestResponse])
async def get_tests():
    # TODO: Заглушка. Позже будет вызов TestService
    return [
        TestResponse(id=1, title="Python Basics", description="Test your Python skills", duration_minutes=30, is_published=True),
        TestResponse(id=2, title="SQL Fundamentals", description="Basic SQL questions", duration_minutes=20, is_published=True),
    ]

@router.post("", response_model=TestResponse)
async def create_test(request: CreateTestRequest):
    # TODO: Заглушка
    return TestResponse(id=99, title=request.title, description=request.description, duration_minutes=request.duration_minutes, is_published=False)
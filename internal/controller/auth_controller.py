from fastapi import APIRouter
from internal.models.auth_models import RegisterRequest, UserResponse, LoginRequest, TokenResponse
from internal.service.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
async def register(request: RegisterRequest):
    return AuthService.register_user(request)

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    return AuthService.login_user(request)
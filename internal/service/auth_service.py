from internal.models.auth_models import RegisterRequest, UserResponse, LoginRequest, TokenResponse

class AuthService:
    @staticmethod
    def register_user(request: RegisterRequest) -> UserResponse:
        # TODO: Здесь будет логика сохранения в БД через Repository
        # Пока возвращаем заглушку
        return UserResponse(id=1, username=request.username, email=request.email)

    @staticmethod
    def login_user(request: LoginRequest) -> TokenResponse:
        # TODO: Здесь будет проверка пароля и генерация JWT
        return TokenResponse(access_token="fake_jwt_token_for_now")
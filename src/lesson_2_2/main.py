from uuid import UUID

from fastapi import BackgroundTasks, Cookie, FastAPI, HTTPException, Response

from src.lesson_2_2.services.cookie_service import (
    audit_log,
    auth,
    get_current_user,
    settings,
)
from src.lesson_2_2.types_def import (
    LoginRequest,
    Message,
    SumRequest,
    SumResponse,
    TypesDemo,
    User,
    UserResponse,
)

cookie_api = FastAPI()


@cookie_api.post("/login", response_model=Message)
def login(
    payload: LoginRequest, response: Response, background: BackgroundTasks
) -> Message:
    """Устанавливает подписанный cookie для пользовательской сессии.

    Args:
        payload (LoginRequest): Данные для входа пользователя (содержит user_id)
        response (Response): HTTP-ответ, в который будет установлен cookie
        background (BackgroundTasks): Фоновые задачи для аудита

    Returns:
        Message: Сообщение об успешном входе
    """
    auth.set_session_cookie(response, payload.user_id)
    background.add_task(audit_log, event="login", user_id=payload.user_id)
    return Message(message="Logged in")


@cookie_api.post("/logout", response_model=Message)
def logout(
    response: Response,
    session: str | None = Cookie(default=None, alias=settings.cookie_name),
) -> Message:
    """Удаляет cookie сессии пользователя.

    Args:
        response (Response): HTTP-ответ, из которого будет удалён cookie
        session (str | None, optional): Значение сессионного cookie. По умолчанию извлекается из запроса.

    Returns:
        Message: Сообщение об успешном выходе
    """
    try:
        if session:
            _ = auth.verify_cookie(session)
    except HTTPException:
        pass
    auth.clear_session_cookie(response)
    return Message(message="Logged out")


@cookie_api.get("/me", response_model=dict)
def me() -> dict:
    """Возвращает идентификатор текущего пользователя из cookie.

    Returns:
        dict: Словарь с user_id текущего пользователя
    """
    user_id: UUID = get_current_user()
    return {"user_id": str(user_id)}


@cookie_api.post("/users", response_model=UserResponse)
async def create_user(user: User) -> dict[str, str | User]:
    """Создаёт пользователя и возвращает подтверждение.

    Args:
        user (User): Данные нового пользователя

    Returns:
        dict[str, str | User]: Словарь с сообщением и созданным пользователем
    """
    return {"message": f"Пользователь {user.name} создан!", "user": user}


@cookie_api.post("/calculate-decimal", response_model=SumResponse)
def calculate_decimal(body: SumRequest) -> SumResponse:
    """Складывает два Decimal и возвращает точный результат.

    Args:
        body (SumRequest): Запрос с двумя числами для сложения

    Returns:
        SumResponse: Результат сложения
    """
    return SumResponse(result=body.num1 + body.num2)


@cookie_api.post("/types-demo", response_model=TypesDemo)
def types_demo(data: TypesDemo) -> TypesDemo:
    """Эхо сложных типов: date/datetime/time/Decimal/UUID/bytes.

    Args:
        data (TypesDemo): Данные с различными типами

    Returns:
        TypesDemo: Те же данные, что были получены
    """
    return data

from datetime import datetime
from typing import Literal, cast
from uuid import UUID

from fastapi import HTTPException, Response, status
from itsdangerous import BadSignature, SignatureExpired, TimestampSigner

from src.lesson_2_2.types_def import Settings

settings = Settings()
signer = TimestampSigner(settings.secret_key)


def sign_value(value: str) -> str:
    """Подписать значение с таймстампом (TTL)."""
    return signer.sign(value).decode("utf-8")


def unsign_value(signed: str, max_age: int) -> str:
    """Проверить подпись и срок действия (TTL) и вернуть исходное значение."""
    return signer.unsign(signed.encode("utf-8"), max_age=max_age).decode("utf-8")


class AuthService:
    """Сервис для работы с подписанными cookie.

    - Установка cookie с подписью и временем жизни (TTL)
    - Проверка валидности и срока действия cookie
    - Удаление cookie
    """

    def __init__(self, *, cookie_name: str, max_age: int) -> None:
        """Конструктор AuthService

        Args:
            cookie_name (str): Имя cookie для хранения сессии пользователя
            max_age (int): Время жизни cookie (TTL) в секундах
        """
        self.cookie_name = cookie_name
        self.max_age = max_age

    def set_session_cookie(self, response: Response, user_id: UUID) -> None:
        """Устанавливает HttpOnly cookie с подписью и временем жизни (TTL).

        Args:
            response (Response): Объект ответа FastAPI
            user_id (UUID): Идентификатор пользователя (UUID)
        """
        signed = sign_value(str(user_id))

        samesite_value: Literal["lax", "strict", "none"] | None = (
            cast(Literal["lax", "strict", "none"], settings.cookie_samesite)
            if settings.cookie_samesite in ("lax", "strict", "none")
            else None
        )
        response.set_cookie(
            key=self.cookie_name,
            value=signed,
            max_age=self.max_age,
            httponly=True,
            secure=settings.cookie_secure,
            samesite=samesite_value,
            path="/",
        )

    def clear_session_cookie(self, response: Response) -> None:
        """Удаляет cookie сессии пользователя.

        Args:
            response (Response): Объект ответа FastAPI
        """
        response.delete_cookie(self.cookie_name)

    def verify_cookie(self, signed_value: str | None) -> UUID:
        """Проверяет подпись и срок действия cookie, возвращает UUID пользователя.

        Args:
            signed_value (str | None): Подписанное значение cookie

        Raises:
            HTTPException: Если cookie отсутствует
            HTTPException: Если истек срок действия cookie
            HTTPException: Если подпись некорректна

        Returns:
            UUID: UUID пользователя
        """
        if not signed_value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="No session cookie"
            )
        try:
            raw = unsign_value(signed_value, max_age=self.max_age)
            return UUID(raw)
        except SignatureExpired:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired"
            )
        except (BadSignature, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session"
            )


def audit_log(event: str, user_id: UUID | None) -> None:
    """Запись аудита события.

    Args:
        event (str): Событие для аудита
        user_id (UUID | None): Идентификатор пользователя (UUID)
    """
    now = datetime.now().isoformat()
    print(f"[AUDIT] {now} user={user_id} event={event}")


def get_current_user(session: str | None = None) -> UUID:
    """Извлечение и проверка текущего пользователя по подписанному cookie.

    Args:
        session (str | None, optional): Сессионный cookie.

    Returns:
        UUID: UUID пользователя
    """
    return auth.verify_cookie(session)


auth = AuthService(cookie_name=settings.cookie_name, max_age=settings.cookie_max_age)

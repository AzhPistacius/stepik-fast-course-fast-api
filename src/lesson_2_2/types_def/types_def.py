from datetime import (  # Эти типы используются для работы с датами и временем.
    date,
    datetime,
    time,
)
from decimal import (
    Decimal,  # Decimal - десятичное число с плавающей точкой, используемое для точных вычислений.
)
from uuid import (
    UUID,  # UUID (Universally Unique Identifier) — универсальный уникальный идентификатор.
)

from pydantic import BaseModel, Field


class User(BaseModel):
    """Модель пользователя."""

    name: str = Field(..., description="Имя пользователя")
    age: int = Field(..., description="Возраст пользователя")


class UserResponse(BaseModel):
    """Ответ при создании пользователя."""

    message: str
    user: User


class LoginRequest(BaseModel):
    """Запрос на вход: идентификатор пользователя."""

    user_id: UUID = Field(..., description="UUID пользователя")


class Message(BaseModel):
    """Простое сообщение-ответ."""

    message: str


class SumRequest(BaseModel):
    """Запрос на сложение точной десятичной арифметикой."""

    num1: Decimal = Field(..., description="Первое число (Decimal)")
    num2: Decimal = Field(..., description="Второе число (Decimal)")


class SumResponse(BaseModel):
    """Ответ со суммой."""

    result: Decimal


class TypesDemo(BaseModel):
    """Демонстрация сложных типов, сериализуемых в JSON."""

    d: date
    dt: datetime
    t: time
    amount: Decimal
    user_id: UUID
    payload: bytes


class Settings(BaseModel):
    """Настройки приложения и политики cookie."""

    secret_key: str = Field(
        default="CHANGE_ME_SUPER_SECRET", description="Секрет для подписи cookie"
    )
    cookie_name: str = Field(default="session", description="Имя cookie сессии")
    cookie_max_age: int = Field(default=3600, description="TTL cookie в секундах")
    cookie_secure: bool = Field(
        default=True, description="Отдавать cookie только по HTTPS"
    )
    cookie_samesite: str = Field(
        default="lax", description="Политика SameSite: lax|strict|none"
    )

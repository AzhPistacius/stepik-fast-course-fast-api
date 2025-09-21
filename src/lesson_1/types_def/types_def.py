from pydantic import BaseModel, Field


class CalculateRequest(BaseModel):
    """Модель входных данных: два числа."""

    num1: float = Field(..., description="Первое число")
    num2: float = Field(..., description="Второе число")


class CalculateResponse(BaseModel):
    """Модель ответа: сумма."""

    result: float

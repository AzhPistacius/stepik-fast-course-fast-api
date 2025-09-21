from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(..., description="Имя пользователя")
    age: int = Field(..., description="Возраст пользователя")


class UserResponse(BaseModel):
    message: str
    user: User

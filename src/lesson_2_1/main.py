from fastapi import FastAPI

from src.lesson_2_1.types_def import User, UserResponse

http_api = FastAPI()

"""
Когда использовать Form, а когда Body?
    Form подходит для обработки данных из HTML-форм
    Body (pydantic.BaseModel) используется, когда данные приходят в формате JSON
"""


@http_api.get("/users")
def get_users() -> dict[str, str]:
    """Эндпоинт для получения списка пользователей.

    Returns:
        dict[str, str]: Словарь с сообщением о списке пользователей
    """
    return {"message": "Список пользователей"}


@http_api.post("/users", response_model=UserResponse)
async def create_user(user: User) -> dict[str, str | User]:
    """Эндпоинт для создания нового пользователя.

    Args:
        user (User): Данные пользователя для создания

    Returns:
        dict[str, str | User]: Словарь с сообщением о создании пользователя и его данными
    """
    return {"message": f"Пользователь {user.name} создан!", "user": user}


@http_api.put("/users/{user_id}")
def update_user(user_id: int) -> dict[str, str]:
    """Эндпоинт для обновления информации о пользователе.

    Args:
        user_id (int): ID пользователя для обновления

    Returns:
        dict[str, str]: Словарь с сообщением об обновлении пользователя
    """
    return {"message": f"Пользователь {user_id} обновлён"}


@http_api.delete("/users/{user_id}")
def delete_user(user_id: int) -> dict[str, str]:
    """Эндпоинт для удаления пользователя.

    Args:
        user_id (int): ID пользователя для удаления

    Returns:
        dict[str, str]: Словарь с сообщением об удалении пользователя
    """
    return {"message": f"Пользователь {user_id} удалён"}


@http_api.options("/")
def options_example() -> dict[str, str]:
    """Эндпоинт для получения доступных методов.

    Returns:
        dict[str, str]: Словарь с сообщением о доступных методах
    """
    return {"message": "Этот запрос проверяет, какие методы доступны"}


@http_api.head("/")
def head_example() -> dict[str, str]:
    """Эндпоинт для получения заголовков ответа без тела.

    Returns:
        dict[str, str]: Словарь с сообщением о заголовках
    """
    return {"message": "Ответ без тела (только заголовки)"}


@http_api.patch("/users/{user_id}")
def patch_user(user_id: int) -> dict[str, str]:
    """Эндпоинт для частичного обновления информации о пользователе.

    Args:
        user_id (int): ID пользователя для частичного обновления

    Returns:
        dict[str, str]: Словарь с сообщением о частичном обновлении пользователя
    """
    return {"message": f"Пользователь {user_id} частично обновлён"}


@http_api.trace("/")
def trace_example() -> dict[str, str]:
    """Эндпоинт для трассировки запроса.

    Returns:
        dict[str, str]: Словарь с сообщением о трассировке
    """
    return {"message": "TRACE-запрос вернёт сам себя"}

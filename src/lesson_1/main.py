from fastapi import FastAPI
from fastapi.responses import FileResponse

from src.lesson_1.types_def import CalculateRequest, CalculateResponse

hello_world_api = FastAPI()


@hello_world_api.get("/hello")
async def hello_endpoint() -> dict[str, str]:
    """Эндпоинт, возвращающий сообщение "Hello World".

    Returns:
        dict[str, str]: Словарь с сообщением "Hello World"
    """
    return {"message": "Hello World"}


@hello_world_api.get("/bye")
async def bye_endpoint() -> FileResponse:
    """Эндпоинт, возвращающий HTML файл с прощальным сообщением.

    Returns:
        FileResponse: HTML файл с прощальным сообщением
    """
    return FileResponse("public/bye.html")


@hello_world_api.post("/calculate", response_model=CalculateResponse)
def calculate_endpoint(payload: CalculateRequest) -> CalculateResponse:
    """Эндпоинт, принимающий два числа и возвращающий их сумму.

    Args:
        payload (CalculateRequest): Входные данные с двумя числами

    Returns:
        CalculateResponse: Ответ с суммой двух чисел
    """
    return CalculateResponse(
        result=payload.num1 + payload.num2
    )  # Просмотреть ответ можно с помощью  Swagger UI по пути /docs

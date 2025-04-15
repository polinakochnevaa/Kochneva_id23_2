from pydantic import BaseModel

class ImageRequest(BaseModel):
    """Запрос на обработку изображения"""
    image: str  # base64 строка
    algorithm: str = "otsu"  # алгоритм обработки

class ImageResponse(BaseModel):
    """Результат обработки"""
    binarized_image: str  # base64 строка
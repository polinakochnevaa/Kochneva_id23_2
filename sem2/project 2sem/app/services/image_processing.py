import cv2
import numpy as np
import base64


def binarize_image_otsu(image_base64: str) -> str:
    """Бинаризация изображения методом Отсу"""
    try:
        # Декодирование base64
        image_data = base64.b64decode(image_base64)
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

        # Применение алгоритма Отсу
        _, binary_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Кодирование результата
        _, buffer = cv2.imencode('.png', binary_img)
        return base64.b64encode(buffer).decode('utf-8')
    except Exception as e:
        raise ValueError(f"Ошибка обработки: {str(e)}")
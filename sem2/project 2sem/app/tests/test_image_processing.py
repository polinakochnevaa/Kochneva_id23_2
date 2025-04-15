from fastapi.testclient import TestClient
import base64
import os


def test_binary_image():
    """Тест обработки изображения"""
    client = TestClient(app)

    # Сначала аутентифицируемся
    login_response = client.post("/auth/login/", data={
        "username": "test@example.com",
        "password": "testpassword"
    })
    token = login_response.json()["access_token"]

    # Читаем тестовое изображение
    with open("test_image.png", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Тестируем endpoint
    response = client.post(
        "/image/binary_image",
        json={"image": encoded_image},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "binarized_image" in response.json()
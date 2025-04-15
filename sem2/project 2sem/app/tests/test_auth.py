from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

client = TestClient(app)

def setup_module():
    """Настройка тестовой базы данных"""
    db = SessionLocal()
    # Очистка тестовых данных
    db.query(User).filter(User.email == "test@example.com").delete()
    db.commit()

def test_sign_up():
    """Тест регистрации пользователя"""
    response = client.post("/auth/sign-up/", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_login():
    """Тест аутентификации пользователя"""
    response = client.post("/auth/login/", data={
        "username": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    email: EmailStr


class UserCreate(UserBase):
    """Схема для создания пользователя"""
    password: str


class User(UserBase):
    """Схема пользователя для ответов API"""
    id: int

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy


class Token(BaseModel):
    """Схема JWT токена"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Данные в JWT токене"""
    email: str | None = None
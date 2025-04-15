from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token
from app.schemas.binary_image import ImageRequest, ImageResponse
from app.services.image_processing import binarize_image_otsu
from app.cruds.user import get_user_by_email
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Обработка изображений"])
security = HTTPBearer()


@router.post("/binary_image", response_model=ImageResponse, summary="Бинаризация")
async def binary_image(
        request: ImageRequest,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    """Обработка изображения методом Отсу"""
    try:
        email = verify_token(credentials.credentials)
        user = get_user_by_email(db, email=email)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        result = binarize_image_otsu(request.image)
        return {"binarized_image": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
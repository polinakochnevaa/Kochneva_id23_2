from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, binary_image

app = FastAPI(title="API для бинаризации изображений")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Аутентификация"])
app.include_router(binary_image.router, prefix="/image", tags=["Изображения"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=2207)
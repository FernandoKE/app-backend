from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
async def hello():
    return {"message": "¡Hola Mundo!"}
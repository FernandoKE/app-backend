from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(router=router, prefix="")

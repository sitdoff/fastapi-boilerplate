import uvicorn
from fastapi import FastAPI

from src.config import settings

app = FastAPI(prefix=settings.app_settings.api_prefix)

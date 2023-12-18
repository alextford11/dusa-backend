from fastapi import FastAPI

from src.dusa_backend.presentation import stats

app = FastAPI()

app.include_router(stats.router)

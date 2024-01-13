from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.dusa_backend.presentation import stats, dashboard, record, category, category_item, location

app = FastAPI()

app.include_router(stats.router)
app.include_router(dashboard.router)
app.include_router(record.router)
app.include_router(category.router)
app.include_router(category_item.router)
app.include_router(location.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://down-under-stats-app.web.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

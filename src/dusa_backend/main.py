from fastapi import FastAPI

from src.dusa_backend.presentation import stats, dashboard, record, category, category_item

app = FastAPI()

app.include_router(stats.router)
app.include_router(dashboard.router)
app.include_router(record.router)
app.include_router(category.router)
app.include_router(category_item.router)

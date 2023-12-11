from fastapi import FastAPI

from src.dusa_backend.presentation import stats

app = FastAPI()

app.include_router(stats.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

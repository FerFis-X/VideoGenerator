# app/main.py
from fastapi import FastAPI
from .api import router as api_router

app = FastAPI(
    title="Math Solver Video Agent MVP",
    description="Resuelve un problema matemático y genera video educativo paso a paso.",
    version="0.1.0",
)

app.include_router(api_router)

# opcional: health check rápido
@app.get("/health")
def health():
    return {"status": "ok"}

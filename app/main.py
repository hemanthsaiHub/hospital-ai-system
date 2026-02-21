from fastapi import FastAPI
from app.core.database import Base, engine
from app.models.user import User  # ← THIS IS THE KEY LINE
from app.routers.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital AI System")

app.include_router(auth_router)

@app.get("/")
def root():
    return {"status": "OK"}

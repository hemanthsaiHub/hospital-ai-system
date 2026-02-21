from fastapi import FastAPI

app = FastAPI(
    title="Hospital Management System with AI",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Hospital AI System is running 🚀"}
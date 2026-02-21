from fastapi import FastAPI
from app.core.database import Base, engine
from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.routers.auth import router as auth_router
from app.routers.doctor import router as doctor_router
from app.routers.patient import router as patient_router
from app.routers.appointment import router as appointment_router
from app.routers.admin import router as admin_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital AI System")

app.include_router(auth_router)
app.include_router(doctor_router)
app.include_router(patient_router)
app.include_router(appointment_router)
app.include_router(admin_router)

@app.get("/", tags=["Root"])  # ← ADD tags=["Root"] HERE
def root():
    return {"status": "OK"}





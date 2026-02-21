from pydantic import BaseModel
from datetime import date, time

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    date: date
    time: time
    reason: str
    status: str = "scheduled"

class AppointmentOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    date: date
    time: time
    reason: str
    status: str

    class Config:
        from_attributes = True
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.deps import get_db
from app.core.security import decode_token
from app.models.appointment import Appointment
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.schemas.appointment import AppointmentCreate, AppointmentOut

router = APIRouter(prefix="/appointments", tags=["Appointments"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user_role(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        return payload.get("role")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def admin_or_doctor(role: str = Depends(get_current_user_role)):
    if role not in ["admin", "doctor"]:
        raise HTTPException(status_code=403, detail="Admins and Doctors only")
    return role


# Book appointment
@router.post("/", response_model=AppointmentOut)
def book_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    new_appointment = Appointment(**appointment.model_dump())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment


# Get all appointments
@router.get("/", response_model=list[AppointmentOut])
def get_appointments(db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    return db.query(Appointment).all()


# Get one appointment
@router.get("/{appointment_id}", response_model=AppointmentOut)
def get_appointment(appointment_id: int, db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


# Update appointment status
@router.put("/{appointment_id}", response_model=AppointmentOut)
def update_appointment(appointment_id: int, data: AppointmentCreate, db: Session = Depends(get_db), role: str = Depends(admin_or_doctor)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    for key, value in data.model_dump().items():
        setattr(appointment, key, value)
    db.commit()
    db.refresh(appointment)
    return appointment


# Cancel appointment
@router.delete("/{appointment_id}")
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appointment.status = "cancelled"
    db.commit()
    return {"message": "Appointment cancelled successfully"}
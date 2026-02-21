from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.deps import get_db
from app.core.security import decode_token
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorOut

router = APIRouter(prefix="/doctors", tags=["Doctors"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user_role(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        return payload.get("role")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def admin_only(role: str = Depends(get_current_user_role)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return role


# Add doctor (admin only)
@router.post("/", response_model=DoctorOut)
def add_doctor(doctor: DoctorCreate, db: Session = Depends(get_db), role: str = Depends(admin_only)):
    existing = db.query(Doctor).filter(Doctor.email == doctor.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Doctor already exists")
    new_doctor = Doctor(**doctor.model_dump())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor


# Get all doctors (any logged in user)
@router.get("/", response_model=list[DoctorOut])
def get_doctors(db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    return db.query(Doctor).all()


# Get one doctor
@router.get("/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: int, db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


# Update doctor (admin only)
@router.put("/{doctor_id}", response_model=DoctorOut)
def update_doctor(doctor_id: int, data: DoctorCreate, db: Session = Depends(get_db), role: str = Depends(admin_only)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    for key, value in data.model_dump().items():
        setattr(doctor, key, value)
    db.commit()
    db.refresh(doctor)
    return doctor


# Delete doctor (admin only)
@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db), role: str = Depends(admin_only)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db.delete(doctor)
    db.commit()
    return {"message": "Doctor deleted successfully"}
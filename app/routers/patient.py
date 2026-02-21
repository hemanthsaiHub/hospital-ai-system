from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.deps import get_db
from app.core.security import decode_token
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientOut

router = APIRouter(prefix="/patients", tags=["Patients"])
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


# Add patient
@router.post("/", response_model=PatientOut)
def add_patient(patient: PatientCreate, db: Session = Depends(get_db), role: str = Depends(admin_or_doctor)):
    existing = db.query(Patient).filter(Patient.email == patient.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Patient already exists")
    new_patient = Patient(**patient.model_dump())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


# Get all patients
@router.get("/", response_model=list[PatientOut])
def get_patients(db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    return db.query(Patient).all()


# Get one patient
@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


# Update patient
@router.put("/{patient_id}", response_model=PatientOut)
def update_patient(patient_id: int, data: PatientCreate, db: Session = Depends(get_db), role: str = Depends(admin_or_doctor)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    for key, value in data.model_dump().items():
        setattr(patient, key, value)
    db.commit()
    db.refresh(patient)
    return patient


# Delete patient (admin only)
@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted successfully"}
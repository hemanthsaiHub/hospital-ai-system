from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.deps import get_db
from app.core.security import decode_token
from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment

router = APIRouter(prefix="/admin", tags=["Admin"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def admin_only(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        role = payload.get("role")
        if role != "admin":
            raise HTTPException(status_code=403, detail="Admins only")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Dashboard summary
@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db), payload: dict = Depends(admin_only)):
    total_users = db.query(User).count()
    total_doctors = db.query(Doctor).count()
    total_patients = db.query(Patient).count()
    total_appointments = db.query(Appointment).count()
    scheduled = db.query(Appointment).filter(Appointment.status == "scheduled").count()
    completed = db.query(Appointment).filter(Appointment.status == "completed").count()
    cancelled = db.query(Appointment).filter(Appointment.status == "cancelled").count()

    return {
        "total_users": total_users,
        "total_doctors": total_doctors,
        "total_patients": total_patients,
        "total_appointments": total_appointments,
        "appointments_by_status": {
            "scheduled": scheduled,
            "completed": completed,
            "cancelled": cancelled
        }
    }


# Get all users
@router.get("/users")
def get_all_users(db: Session = Depends(get_db), payload: dict = Depends(admin_only)):
    users = db.query(User).all()
    return [{"id": u.id, "email": u.email, "role": u.role} for u in users]


# Delete user
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), payload: dict = Depends(admin_only)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


# Change user role
@router.put("/users/{user_id}/role")
def change_user_role(user_id: int, new_role: str, db: Session = Depends(get_db), payload: dict = Depends(admin_only)):
    if new_role not in ["admin", "doctor", "nurse", "user"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = new_role
    db.commit()
    return {"message": f"Role updated to {new_role}"}


# Get all appointments (admin view)
@router.get("/appointments")
def get_all_appointments(db: Session = Depends(get_db), payload: dict = Depends(admin_only)):
    appointments = db.query(Appointment).all()
    return appointments


# Get recent patients
@router.get("/patients/recent")
def get_recent_patients(db: Session = Depends(get_db), payload: dict = Depends(admin_only)):
    patients = db.query(Patient).order_by(Patient.id.desc()).limit(10).all()
    return patients
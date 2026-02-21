from pydantic import BaseModel, EmailStr

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    phone: str
    email: EmailStr

class DoctorOut(BaseModel):
    id: int
    name: str
    specialization: str
    phone: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
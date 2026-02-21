from pydantic import BaseModel, EmailStr

class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    phone: str
    email: EmailStr
    blood_group: str
    address: str

class PatientOut(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    phone: str
    email: EmailStr
    blood_group: str
    address: str

    class Config:
        from_attributes = True
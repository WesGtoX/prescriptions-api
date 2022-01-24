from pydantic import BaseModel


class Base(BaseModel):
    id: int


class Clinic(Base):
    pass


class Patient(Base):
    pass


class Physician(Base):
    pass


class PrescriptionCreate(BaseModel):
    clinic: Clinic
    physician: Patient
    patient: Physician
    text: str


class Prescription(PrescriptionCreate):
    id: int

    class Config:
        orm_mode = True

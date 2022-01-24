from pydantic import BaseModel


class Base(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Clinic(Base):
    pass


class Patient(Base):
    name: str
    email: str
    phone: str


class Physician(Base):
    crm: str

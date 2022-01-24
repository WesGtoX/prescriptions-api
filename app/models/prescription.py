from sqlalchemy import Column, Integer, String

from app.db import Base


class Prescription(Base):

    __tablename__ = 'prescriptions'

    id = Column(Integer, primary_key=True, index=True)
    clinic_id = Column(Integer, index=True)
    physician_id = Column(Integer, index=True)
    patient_id = Column(Integer, index=True)
    text = Column(String, index=True)

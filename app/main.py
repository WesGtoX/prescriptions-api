from typing import Dict
from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from app import crud, schemas, dependencies, docs
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Prescriptions API',
    description='API to insert new prescriptions.',
)


@app.get('/', responses={200: docs.RESPONSES_EXAMPLE.get('hello_world')}, tags=['hello_world'])
def hello_world() -> Dict[str, str]:
    return {'hello_world': 'Prescriptions API'}


@app.post('/prescriptions/', response_model=schemas.Prescription, status_code=status.HTTP_201_CREATED, tags=['prescriptions'])
async def create_prescription(prescription: schemas.PrescriptionCreate, db: Session = Depends(dependencies.get_db)) -> schemas.Prescription:
    db_prescription = crud.Prescription(db=db)
    return await db_prescription.process(prescription=prescription)

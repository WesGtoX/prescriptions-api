import asyncio
import logging
import aiohttp

from typing import Dict, Any
from sqlalchemy.orm import Session

from app import models, schemas
from app.core.config import settings
from app.crud.dependent_crud import Dependents
from app.schemas.dependent import Physician, Patient, Clinic

logger = logging.getLogger(__name__)

METHODS = ['physician', 'clinic', 'patient']


class Prescription:

    def __init__(self, redis, db: Session) -> None:
        self.redis = redis
        self.db = db

    @staticmethod
    def format_data(prefix: str, values: Dict[str, Any]) -> Dict[str, int]:
        return {prefix + str(key): val for key, val in values.items()}

    @staticmethod
    def parse_data(prescription: schemas.PrescriptionCreate) -> Dict[str, int]:
        return dict(
            clinic_id=prescription.clinic.id,
            physician_id=prescription.physician.id,
            patient_id=prescription.patient.id,
            text=prescription.text,
        )

    def create(self, data: models.Prescription) -> None:
        self.db.add(data)

    def commit(self, data: models.Prescription) -> None:
        self.db.commit()
        self.db.refresh(data)

    def rollback(self) -> None:
        self.db.rollback()

    def pase_metrics_data(self, prescription: models.Prescription, dependents: Dependents) -> Dict[str, int]:
        physician = Physician(**dependents.dependent.get('physician'))
        patient = Patient(**dependents.dependent.get('patient'))

        metrics = {}
        metrics.update(self.format_data('physician_', physician.dict()))
        metrics.update(self.format_data('patient_', patient.dict()))
        metrics.update({'prescription_id': prescription.id})

        if dependents.dependent.get('clinic'):
            clinic = Clinic(**dependents.dependent.get('clinic'))
            clinic_data = self.format_data('clinic_', clinic.dict())
            metrics.update(clinic_data)

        return metrics

    def create_prescription(self, data: Dict[str, int]) -> models.Prescription:
        return models.Prescription(**data)

    async def save_metrics(self, prescription: models.Prescription, dependents: Dependents) -> aiohttp.ClientResponse:
        try:
            data = self.pase_metrics_data(prescription, dependents)
            return await dependents.post_metrics(data=data)
        except (aiohttp.ClientResponseError, aiohttp.ClientConnectorError) as e:
            raise e

    async def create_metrics(self, prescription: models.Prescription) -> aiohttp.ClientResponse:
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            try:
                dependents = Dependents(
                    redis=self.redis, session=session,
                    base_uri=settings.DEPENDENT_SERVICES_URL
                )
                tasks = [
                    asyncio.create_task(
                        getattr(dependents, f'get_{m}')(getattr(prescription, f'{m}_id'))
                    ) for m in METHODS
                ]
                await asyncio.gather(*tasks)

                return await self.save_metrics(prescription, dependents)
            except (aiohttp.ClientResponseError, aiohttp.ClientConnectorError) as e:
                self.rollback()
                logger.error(e)
                raise e

    async def process(self, prescription: schemas.PrescriptionCreate) -> schemas.Prescription:
        prescription_data = self.parse_data(prescription)
        db_prescription = self.create_prescription(prescription_data)

        self.create(db_prescription)
        await self.create_metrics(db_prescription)
        self.commit(db_prescription)

        return schemas.Prescription(id=db_prescription.id, **prescription.dict())

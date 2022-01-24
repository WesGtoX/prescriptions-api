import logging
from typing import Dict

import aiohttp
import backoff
from fastapi import HTTPException

from app.core.config import settings

logging.getLogger('backoff').addHandler(logging.StreamHandler())
logger = logging.getLogger(__name__)

TIMEOUT = {'physician': 4, 'clinic': 5, 'patient': 3, 'metrics': 6}
RETRY = {'physician': 2, 'clinic': 3, 'patient': 2, 'metrics': 5}
AUTH = settings.DEPENDENT_SERVICES_AUTH


class Dependents:

    def __init__(self, session: aiohttp.ClientSession, base_uri: str) -> None:
        self.session = session
        self.base_uri = base_uri
        self.dependent = {}

    @backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=RETRY.get('physician'))
    async def get_physician(self, physician_id: int):
        try:
            headers = {'Authentication': f'Bearer {AUTH.get("physician")}'}
            url = f'{self.base_uri}/physicians/{physician_id}'
            async with await self.session.get(url=url, headers=headers, timeout=TIMEOUT.get('physician')) as response:
                self.dependent['physician'] = await response.json()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            if hasattr(e, 'status') and getattr(e, 'status') == 404:
                raise HTTPException(status_code=404, detail=dict(message='physician not found', code='02'))

            raise HTTPException(status_code=400, detail=dict(message='physicians service not available', code='05'))

    @backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=RETRY.get('clinic'))
    async def get_clinic(self, clinic_id: int):
        try:
            headers = {'Authentication': f'Bearer {AUTH.get("clinic")}'}
            url = f'{self.base_uri}/clinics/{clinic_id}'
            async with await self.session.get(url=url, headers=headers, timeout=TIMEOUT.get('clinic')) as response:
                self.dependent['clinic'] = await response.json()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            logger.error(e)

    @backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=RETRY.get('patient'))
    async def get_patient(self, patient_id: int):
        try:
            headers = {'Authentication': f'Bearer {AUTH.get("patient")}'}
            url = f'{self.base_uri}/patients/{patient_id}'
            async with await self.session.get(url=url, headers=headers, timeout=TIMEOUT.get('patient')) as response:
                self.dependent['patient'] = await response.json()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            if hasattr(e, 'status') and getattr(e, 'status') == 404:
                raise HTTPException(status_code=404, detail=dict(message='patients service not available', code='03'))

            raise HTTPException(status_code=400, detail=dict(message='patients service not available', code='06'))

    @backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=RETRY.get('metrics'))
    async def post_metrics(self, data: Dict[str, int]):
        try:
            headers = {'Authentication': f'Bearer {AUTH.get("metrics")}'}
            url = f'{self.base_uri}/metrics/'
            async with await self.session.post(url=url, data=data, headers=headers,
                                               timeout=TIMEOUT.get('metrics')) as response:
                return await response.json()
        except aiohttp.ClientResponseError:
            raise HTTPException(status_code=400, detail=dict(message='metrics service not available', code='04'))

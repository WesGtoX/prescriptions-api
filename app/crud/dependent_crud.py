import logging
from typing import Dict

import aiohttp
import backoff
from fastapi import HTTPException, status

from app.core.config import settings
from app.db.redis import get_redis, set_redis

logging.getLogger('backoff').addHandler(logging.StreamHandler())
logger = logging.getLogger(__name__)

TIMEOUT = {'physician': 4, 'clinic': 5, 'patient': 3, 'metrics': 6}
RETRY = {'physician': 2, 'clinic': 3, 'patient': 2, 'metrics': 5}


class Dependents:

    def __init__(self, redis, session: aiohttp.ClientSession, base_uri: str) -> None:
        self.redis = redis
        self.session = session
        self.base_uri = base_uri
        self.dependent: Dict[str, int] = {}

    @backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=RETRY.get('physician'))
    async def get_physician(self, physician_id: int) -> aiohttp.ClientResponse:
        try:
            value = await get_redis(redis=self.redis, name='physician')
            if value:
                self.dependent['physician'] = value
                return value

            headers = {'Authentication': f'Bearer {settings.PHYSICIANS_AUTH}'}
            url = f'{self.base_uri}/physicians/{physician_id}'
            async with await self.session.get(url=url, headers=headers, timeout=TIMEOUT.get('physician')) as response:
                self.dependent['physician'] = await response.json()
                await set_redis(
                    redis=self.redis, name='physician',
                    mapping=self.dependent.get('physician'),
                    expires=settings.TTL_PHYSICIAN
                )
                return await response.json()
        except (aiohttp.ClientResponseError, aiohttp.ClientConnectorError) as e:
            if hasattr(e, 'status') and getattr(e, 'status') == status.HTTP_404_NOT_FOUND:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=dict(message='physician not found', code='02')
                )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=dict(message='physicians service not available', code='05')
            )

    @backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=RETRY.get('clinic'))
    async def get_clinic(self, clinic_id: int) -> aiohttp.ClientResponse | Dict:
        try:
            value = await get_redis(redis=self.redis, name='clinic')
            if value:
                self.dependent['clinic'] = value
                return value

            headers = {'Authentication': f'Bearer {settings.CLINICS_AUTH}'}
            url = f'{self.base_uri}/clinics/{clinic_id}'
            async with await self.session.get(url=url, headers=headers, timeout=TIMEOUT.get('clinic')) as response:
                self.dependent['clinic'] = await response.json()
                await set_redis(
                    redis=self.redis, name='clinic',
                    mapping=self.dependent.get('clinic'),
                    expires=settings.TTL_CLINIC
                )
                return await response.json()
        except (aiohttp.ClientResponseError, aiohttp.ClientConnectorError) as e:
            logger.error(e)
            return {}

    @backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=RETRY.get('patient'))
    async def get_patient(self, patient_id: int) -> aiohttp.ClientResponse:
        try:
            value = await get_redis(redis=self.redis, name='patient')
            if value:
                self.dependent['patient'] = value
                return value

            headers = {'Authentication': f'Bearer {settings.PATIENTS_AUTH}'}
            url = f'{self.base_uri}/patients/{patient_id}'
            async with await self.session.get(url=url, headers=headers, timeout=TIMEOUT.get('patient')) as response:
                self.dependent['patient'] = await response.json()
                await set_redis(
                    redis=self.redis, name='patient',
                    mapping=self.dependent.get('patient'),
                    expires=settings.TTL_PATIENT
                )
                return await response.json()
        except (aiohttp.ClientResponseError, aiohttp.ClientConnectorError) as e:
            if hasattr(e, 'status') and getattr(e, 'status') == status.HTTP_404_NOT_FOUND:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=dict(message='patient not found', code='03')
                )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=dict(message='patients service not available', code='06')
            )

    @backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=RETRY.get('metrics'))
    async def post_metrics(self, data: Dict[str, int]) -> aiohttp.ClientResponse:
        try:
            headers = {'Authentication': f'Bearer {settings.METRICS_AUTH}'}
            url = f'{self.base_uri}/metrics/'
            async with await self.session.post(url=url, data=data, headers=headers,
                                               timeout=TIMEOUT.get('metrics')) as response:
                return await response.json()
        except (aiohttp.ClientResponseError, aiohttp.ClientConnectorError) as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=dict(message='metrics service not available', code='04')
            )

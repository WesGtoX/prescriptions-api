import pytest

from unittest import mock
from aiohttp import ClientSession

from app.core import settings
from app.crud.dependent_crud import Dependents
from tests import fixture

base_uri = 'https://mock-api-challenge.dev.iclinic.com.br'


@pytest.mark.asyncio
@mock.patch('app.crud.dependent_crud.Dependents.get_physician', return_value=fixture.physician_mock)
async def test_get_physician(mock_get_physician, monkeypatch, redis) -> None:
    monkeypatch.setattr(settings, 'DEPENDENT_SERVICES_URL', base_uri)

    async with ClientSession() as session:
        dependent = Dependents(redis, session, base_uri)
        await dependent.get_physician(physician_id=1)
        assert mock_get_physician.call_count == 1
        assert mock_get_physician.return_value == fixture.physician_mock


@pytest.mark.asyncio
@mock.patch('app.crud.dependent_crud.Dependents.get_clinic', return_value=fixture.clinic_mock)
async def test_get_clinic(mock_get_clinic, monkeypatch, redis) -> None:
    monkeypatch.setattr(settings, 'DEPENDENT_SERVICES_URL', base_uri)

    async with ClientSession() as session:
        dependent = Dependents(redis, session, base_uri)
        await dependent.get_clinic(clinic_id=1)
        assert mock_get_clinic.call_count == 1
        assert mock_get_clinic.return_value == fixture.clinic_mock


@pytest.mark.asyncio
@mock.patch('app.crud.dependent_crud.Dependents.get_patient', return_value=fixture.patient_mock)
async def test_get_patient(mock_get_patient, monkeypatch, redis) -> None:
    monkeypatch.setattr(settings, 'DEPENDENT_SERVICES_URL', base_uri)

    async with ClientSession() as session:
        dependent = Dependents(redis, session, base_uri)
        await dependent.get_patient(patient_id=1)
        assert mock_get_patient.call_count == 1
        assert mock_get_patient.return_value == fixture.patient_mock


@pytest.mark.asyncio
@mock.patch('app.crud.dependent_crud.Dependents.post_metrics', return_value=fixture.metrics_mock)
async def test_post_metrics(mock_post_metrics, monkeypatch, redis) -> None:
    monkeypatch.setattr(settings, 'DEPENDENT_SERVICES_URL', base_uri)

    data = {
        'clinic_id': 1,
        'clinic_name': 'iClinic',
        'physician_id': 1,
        'physician_name': 'Myrl',
        'physician_crm': 'KO12HFG',
        'patient_id': 1,
        'patient_name': 'Nathan DuBuque',
        'patient_email': 'Nathan.DuBuque@hotmail.com',
        'patient_phone': '1-938-598-1311',
        'prescription_id': 1,
    }
    async with ClientSession() as session:
        dependent = Dependents(redis, session, base_uri)
        await dependent.post_metrics(data=data)
        assert mock_post_metrics.call_count == 1
        assert mock_post_metrics.return_value == fixture.metrics_mock


@pytest.mark.asyncio
async def test_get_physician_cache(redis) -> None:
    async with ClientSession() as session:
        name, mapping = 'physician', {'foo': 1, 'bar': 2}
        await redis.hmset(name, mapping)

        dependent = Dependents(redis, session, base_uri)
        result = await dependent.get_physician(physician_id=1)
        assert result == {b'foo': b'1', b'bar': b'2'}


@pytest.mark.asyncio
async def test_get_clinic_cache(redis) -> None:
    async with ClientSession() as session:
        name, mapping = 'clinic', {'fizz': 3, 'buzz': 4}
        await redis.hmset(name, mapping)

        dependent = Dependents(redis, session, base_uri)
        result = await dependent.get_clinic(clinic_id=1)
        assert result == {b'fizz': b'3', b'buzz': b'4'}


@pytest.mark.asyncio
async def test_get_patient_cache(redis) -> None:
    async with ClientSession() as session:
        name, mapping = 'patient', {'bar': 5, 'buzz': 6}
        await redis.hmset(name, mapping)

        dependent = Dependents(redis, session, base_uri)
        result = await dependent.get_patient(patient_id=1)
        assert result == {b'bar': b'5', b'buzz': b'6'}

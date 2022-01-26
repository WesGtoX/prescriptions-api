import pytest

from fastapi import status

from app.core import settings
from app.crud import Prescription
from app.crud.dependent_crud import Dependents
from tests import fixture

base_uri = 'https://mock-api-challenge.dev.iclinic.com.br'

data = {
    'clinic': {
        'id': 1
    },
    'physician': {
        'id': 1
    },
    'patient': {
        'id': 1
    },
    'text': 'Dipirona 1x ao dia'
}


@pytest.mark.asyncio
async def test_create_prescription(mocker, test_client, redis) -> None:
    mocker.patch.object(Prescription, 'commit', return_value=True)
    mocker.patch.object(Prescription, 'create_prescription', return_value=fixture.prescription_mock)
    mocker.patch.object(Dependents, 'post_metrics', return_value=fixture.metrics_mock)

    redis.flushall()
    response = test_client.post('/prescriptions/', json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert type(response.json().get('id')) == int
    assert response.json().get('clinic') == data.get('clinic')
    assert response.json().get('physician') == data.get('physician')
    assert response.json().get('patient') == data.get('patient')
    assert response.json().get('text') == data.get('text')


@pytest.mark.asyncio
async def test_physicians_service_not_available(monkeypatch, test_client, redis) -> None:
    monkeypatch.setattr(settings, 'DEPENDENT_SERVICES_URL', 'http://test')

    redis.flushall()
    response = test_client.post('/prescriptions/', json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': {'message': 'physicians service not available', 'code': '05'}}


@pytest.mark.asyncio
async def test_patients_service_not_available(monkeypatch, test_client, redis) -> None:
    monkeypatch.setattr(settings, 'DEPENDENT_SERVICES_URL', 'http://test')

    redis.flushall()
    name, mapping = 'physician', {'foo': 1, 'bar': 2}
    await redis.hmset(name, mapping)

    response = test_client.post('/prescriptions/', json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': {'message': 'patients service not available', 'code': '06'}}


@pytest.mark.asyncio
async def test_metrics_service_not_available(test_client, redis) -> None:
    redis.flushall()
    response = test_client.post('/prescriptions/', json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': {'message': 'metrics service not available', 'code': '04'}}


def test_hello_world(test_client) -> None:
    response = test_client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'hello_world': 'Prescriptions API'}

from app.schemas.prescription import Prescription
from app.schemas.dependent import Clinic, Physician, Patient


def test_prescription() -> None:
    data = dict(id=1, clinic={'id': 1}, physician={'id': 1}, patient={'id': 1}, text='Dipirona 1x ao dia')
    prescription = Prescription(**data)
    assert prescription.id == data.get('id')
    assert prescription.clinic.id == data.get('clinic').get('id')
    assert prescription.physician.id == data.get('physician').get('id')
    assert prescription.patient.id == data.get('patient').get('id')
    assert prescription.text == data.get('text')


def test_dependents_clinic() -> None:
    data = dict(id=1, name='iClinic')
    clinic = Clinic(**data)
    assert clinic.id == data.get('id')
    assert clinic.name == data.get('name')


def test_dependents_patient() -> None:
    data = dict(id=1, name='Bruce Wayne', email='bruce@wayne.com', phone='+5516999999999')
    patient = Patient(**data)
    assert patient.id == data.get('id')
    assert patient.name == data.get('name')
    assert patient.phone == data.get('phone')
    assert patient.email == data.get('email')


def test_dependents_physician() -> None:
    data = dict(id=1, name='Dr. Strange', crm='123456')
    physician = Physician(**data)
    assert physician.id == data.get('id')
    assert physician.name == data.get('name')
    assert physician.crm == data.get('crm')

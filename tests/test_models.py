from app.models import Prescription


def test_model() -> None:
    data = {
        'clinic_id': 1,
        'physician_id': 1,
        'patient_id': 1,
        'text': 'Dipirona 1x ao dia'
    }
    result = Prescription(**data)
    assert result.clinic_id == data.get('clinic_id')
    assert result.physician_id == data.get('physician_id')
    assert result.patient_id == data.get('patient_id')
    assert result.text == data.get('text')

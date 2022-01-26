from app.models import Prescription

physician_mock = {
    'id': '1',
    'name': 'Myrl',
    'crm': 'KO12HFG',
}

clinic_mock = {
    'id': '1',
    'name': 'iClinic',
}

patient_mock = {
    'id': '1',
    'name': 'Nathan DuBuque',
    'email': 'Nathan.DuBuque@hotmail.com',
    'phone': '1-938-598-1311',
}

metrics_mock = {
    'id': '1',
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

prescription_mock = Prescription(**dict(id=1, clinic_id=1, physician_id=1, patient_id=1, text='Dipirona 1x ao dia'))

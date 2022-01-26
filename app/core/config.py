from pydantic import BaseSettings
from decouple import config


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = config('DATABASE_URL', default='sqlite:///./prescriptions.db')
    REDIS_URL: str = config('REDIS_URL', default='redis://localhost')

    DEPENDENT_SERVICES_URL: str = config(
        'DEPENDENT_SERVICES_URL', default='https://mock-api-challenge.dev.iclinic.com.br'
    )

    PHYSICIANS_AUTH: str = config('PHYSICIANS_AUTH', default='')
    CLINICS_AUTH: str = config('CLINICS_AUTH', default='')
    PATIENTS_AUTH: str = config('PATIENTS_AUTH', default='')
    METRICS_AUTH: str = config('METRICS_AUTH', default='')

    TTL_PHYSICIAN: int = config('TTL_PHYSICIAN', default=172800)  # 48h
    TTL_CLINIC: int = config('TTL_CLINIC', default=259200)  # 72h
    TTL_PATIENT: int = config('TTL_PATIENT', default=43200)  # 12h

    class Config:
        env_file = '.env'


settings = Settings()

import ast

from typing import Dict
from pydantic import BaseSettings
from decouple import config

# def env_to_dict(env: str) -> Dict[Any, Any]:
#     return json.loads(env)
# import ast
# my_dict = ast.literal_eval(TESTING_BROWSERS)


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = config('DATABASE_URL', default='')
    DEPENDENT_SERVICES_URL: str = config('DEPENDENT_SERVICES_URL', default='')
    DEPENDENT_SERVICES_AUTH: Dict[str, str] = ast.literal_eval(config('DEPENDENT_SERVICES_AUTH', default='{}'))

    class Config:
        env_file = '.env'


settings = Settings()

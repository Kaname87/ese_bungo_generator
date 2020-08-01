import os
from uuid import UUID
from dotenv import load_dotenv

def load_env():
    dotenv_path = os.path.dirname(__file__) + '/.env'
    load_dotenv(dotenv_path)

def is_uuid(uuid_string, version=4):
    try:
        val = UUID(uuid_string, version=version)
    except ValueError:
        return False
    return True

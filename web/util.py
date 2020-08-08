import os
import json
import datetime
from uuid import UUID
from dotenv import load_dotenv

class AppModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

def model_to_json(model):
    return model_dict_to_json(model.to_dict())

def model_dict_to_json(dict):
    return json.dumps(dict, cls=AppModelEncoder)

def load_env():
    dotenv_path = os.path.dirname(__file__) + '/.env'
    load_dotenv(dotenv_path)

def is_uuid(uuid_string, version=4):
    try:
        val = UUID(uuid_string, version=version)
    except ValueError:
        return False
    return True

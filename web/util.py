import os
import json
from uuid import UUID
from dotenv import load_dotenv



class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)

def has_uuid_dict_to_json(dict):
    return json.dumps(dict, cls=UUIDEncoder)

def load_env():
    dotenv_path = os.path.dirname(__file__) + '/.env'
    load_dotenv(dotenv_path)

def is_uuid(uuid_string, version=4):
    try:
        val = UUID(uuid_string, version=version)
    except ValueError:
        return False
    return True

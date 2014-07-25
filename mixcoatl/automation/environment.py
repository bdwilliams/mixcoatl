"""Implements the ability to list CM environments via the API"""
from mixcoatl.resource import Resource

class Environment(Resource):
    """An DCM environment represents a Chef environment and is managed in a 
    configuration management account. """
    PATH = 'automation/Environment'
    COLLECTION_NAME = 'environments'
    PRIMARY_KEY = 'environment_id'

    def __init__(self):
        Resource.__init__(self)

    @classmethod
    def all(cls, cm_account_id):
        """List CM environments."""
        res = Resource(cls.PATH)
        res.request_details = 'basic'
        params = {'cmAccountId':cm_account_id}
        cme = res.get(params=params)
        if res.last_error is None:
            return cme[cls.COLLECTION_NAME]
        else:
            return res.last_error

class EnvironmentException(BaseException): 
    """Environment Exception"""
    pass
"""
mixcoatl.automation.personality
--------------------
"""
from mixcoatl.resource import Resource

class Personality(Resource):
    """An Enstratius personality represents an ordered collection of scripts 
    and/or personalities that are executed in an environment to bring a server
    to fit a certain role."""
    PATH = 'automation/Personality'
    COLLECTION_NAME = 'personalities'
    PRIMARY_KEY = 'cmAccountId'

    def __init__(self, cm_account_id = None):
        Resource.__init__(self)
        self.__cm_account_id = cm_account_id 

    @property
    def cm_account_id(self):
        """The configuration management account in which this personality is 
        stored."""
        return self.__cm_account_id

    @classmethod
    def all(cls, cm_account_id):
        """List all personalities."""
        res = Resource(cls.PATH)
        res.request_details = 'basic'
        params = {'cmAccountId':cm_account_id}
        pers = res.get(params=params)
        if res.last_error is None:
            return pers[cls.COLLECTION_NAME]
        else:
            raise PersonalityException(res.last_error)

class PersonalityException(BaseException): 
    """Personality Exception"""
    pass
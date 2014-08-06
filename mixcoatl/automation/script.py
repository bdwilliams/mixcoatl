"""
mixcoatl.automation.script
--------------------
"""
from mixcoatl.resource import Resource

class Script(Resource):
    """An DCM script represents some kind of scriptable item of code 
    managed in a CM account. It may or may not actually be what you would think
    of as a shell script. How DCM maps a 'script' to a specific CM account 
    depends on the underlying CM system. A Chef script is a recipe and a Puppet
    script is a class. An Object Store script is an executable file."""
    PATH = 'automation/Script'
    COLLECTION_NAME = 'scripts'
    PRIMARY_KEY = 'cmAccountId'

    def __init__(self, cm_account_id = None):
        Resource.__init__(self)
        self.__cm_account_id = cm_account_id 

    @property
    def cm_account_id(self):
        """The CM account in which this script is stored."""
        return self.__cm_account_id

    @classmethod
    def all(cls, cm_account_id):
        """List all CM Scripts."""
        res = Resource(cls.PATH)
        res.request_details = 'basic'
        params = {'cmAccountId':cm_account_id}
        scripts = res.get(params=params)
        return scripts[cls.COLLECTION_NAME]

class ScriptException(BaseException): 
    """Script Exception"""
    pass
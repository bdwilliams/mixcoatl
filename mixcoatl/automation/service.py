"""
mixcoatl.automation.service
--------------------
"""
from mixcoatl.resource import Resource
from mixcoatl.decorators.lazy import lazy_property
from mixcoatl.utils import camelize

# pylint: disable-msg=R0902,R0904
class Service(Resource):
    """A service is a programmatic component of a deployment. It can be your 
    MySQL database engine, your Tomcat application service, or any other 
    program that must be managed by DCM."""
    PATH = 'automation/Service'
    COLLECTION_NAME = 'services'
    PRIMARY_KEY = 'service_id'

    def __init__(self, service_id=None, **kwargs):
        Resource.__init__(self)
        self.__service_id = service_id
        self.__backup_interval_in_minutes = None
        self.__budget = None
        self.__description = None
        self.__name = None
        self.__owning_group = None
        self.__owning_user = None
        self.__status = None

    @property
    def service_id(self):
        """The DCM ID of the service."""
        return self.__service_id

    @lazy_property
    def backup_interval_in_minutes(self):
        """The frequency of automated service backups in minutes."""
        return self.__backup_interval_in_minutes

    @lazy_property
    def budget(self):
        """The DCM ID of the budget under which charges associated with this 
        script are billed."""
        return self.__budget

    @lazy_property
    def description(self):
        """A detailed description of the script."""
        return self.__description

    @lazy_property
    def name(self):
        """The shell-level name of this script as stored in the CM system."""
        return self.__name

    @lazy_property
    def owning_group(self):
        """The group or groups that own this script for access control 
        purposes."""
        return self.__owning_group

    @lazy_property
    def owning_user(self):
        """The user to whom this account belongs."""
        return self.__owning_user

    @lazy_property
    def status(self):
        """The current status of the script."""
        return self.__status

    @classmethod
    def all(cls, **kwargs):
        """List all CM scripts."""
        res = Resource(cls.PATH)
        if 'details' in kwargs:
            res.request_details = kwargs['details']
        else:
            res.request_details = 'basic'

        scripts = res.get()
        if res.last_error is None:
            return [cls(i[camelize(cls.PRIMARY_KEY)]) \
            for i in scripts[cls.COLLECTION_NAME]]
        else:
            return res.last_error

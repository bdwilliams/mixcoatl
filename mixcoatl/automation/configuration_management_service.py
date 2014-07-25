"""
mixcoatl.automation.configuration_management_service
--------------------
"""
from mixcoatl.resource import Resource
from mixcoatl.decorators.lazy import lazy_property
from mixcoatl.decorators.validations import required_attrs
from mixcoatl.utils import camelize, camel_keys
import json

# pylint: disable-msg=R0902,R0904
class ConfigurationManagementService(Resource):
    """A configuration management service is an actual service endpoint running 
    a supported configuration management system. Some services like the public 
    OpsCode Platform for Chef may be available to all customers, or you may 
    define your own configuration management service for your company’s 
    private use."""
    PATH = 'automation/ConfigurationManagementService'
    COLLECTION_NAME = 'cmServices'
    PRIMARY_KEY = 'cm_system_id'

    def __init__(self, **kwargs):
        Resource.__init__(self)
        self.__cm_system = None
        self.__service_endpoint = None
        self.__properties = None
        self.__cm_service_id = None
        self.__removable = None
        self.__customer = None
        self.endpoint = None
        self.cm_system_id = None
        self.__name = None
        self.__budget = None
        self.__description = None

    @lazy_property
    def cm_system(self):
        """The configuration management software behind this service."""
        return self.__cm_system

    @lazy_property
    def service_endpoint(self):
        """The http endpoint of the configuration management service. This 
        could be the endpoint of a Chef server API, a Puppet master agent, or a 
        cloud storage API."""
        return self.__service_endpoint

    @lazy_property
    def properties(self):
        """A list of system-specific properties that support connectivity to 
        the service in question."""
        return self.__properties
                
    @lazy_property
    def cm_service_id(self):
        """The unique ID of this configuration management service."""
        return self.__cm_service_id

    @lazy_property
    def budget(self):
        """For private configuration management services, the default budget 
        against which new accounts get billed. Currently not used."""
        return self.__budget

    @budget.setter
    def budget(self, budget):
        """Sets the budget"""
        self.__budget = budget

    @lazy_property
    def removable(self):
        """Identifies whether a service can be de-activated in DCM."""
        return self.__removable
                             
    @lazy_property
    def description(self):
        """A detailed description of the configuration management service."""
        return self.__description

    @description.setter
    def description(self, desc):
        """Sets the description."""
        self.__description = desc

    @lazy_property
    def name(self):
        """The user-friendly name for the configuration management service."""
        return self.__name

    @name.setter
    def name(self, name):
        """Sets the name."""
        self.__name = name

    @lazy_property
    def customer(self):
        """The customer who owns this private CM service."""
        return self.__customer

    @required_attrs(['budget', 
                    'description', 
                    'name', 
                    'endpoint', 
                    'cm_system_id'])
    def create(self):
        """Creates a new CM service."""

        parms = [{"budget": self.budget,
                  "serviceEndpoint": self.endpoint,
                  "description": self.description,
                  "name": self.name,
                  "label": "red",
                  "cmSystem": {"cmSystemID": self.cm_system_id}}]

        payload = {"addService": camel_keys(parms)}
        print json.dumps(payload)

        response = self.post(data=json.dumps(payload))
        if self.last_error is None:
            self.load()
            return response
        else:
            raise CMCreationException(self.last_error)
        
    @classmethod
    def all(cls, **kwargs):
        """List CM Services"""
        res = Resource(cls.PATH)
        if 'details' in kwargs:
            res.request_details = kwargs['details']
        else:
            res.request_details = 'basic'

        cms = res.get()
        if res.last_error is None:
            return [cls(i[camelize(cls.PRIMARY_KEY)]) \
            for i in cms[cls.COLLECTION_NAME]]
        else:
            return res.last_error

class CMException(BaseException): 
    """CM Exception"""
    pass
	
class CMCreationException(CMException):
    """CM Creation Exception"""
    pass
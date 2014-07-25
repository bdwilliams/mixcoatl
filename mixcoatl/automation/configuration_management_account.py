"""
mixcoatl.automation.configuration_management_account
--------------------
"""
from mixcoatl.resource import Resource
from mixcoatl.decorators.lazy import lazy_property
from mixcoatl.utils import camelize

# pylint: disable-msg=R0902,R0904
class ConfigurationManagementAccount(Resource):
    """A configuration management account is an account with a configuration 
    management service. A typical DCM installation will have any number 
    of configuration management services for different configuration management 
    systems (Chef, Puppet, etc.) installed.  DCM also supports 
    customer-owned configuration management services as well. A configuration 
    management account is simply an account in one of these services. For 
    example, you might set up two Chef repositories—one in the OpsCode platform 
    and one inside your data center. You would therefore two configuration 
    management accounts in DCM tied to two different configuration 
    management services, both based on the single Chef configuration management 
    system."""
    PATH = 'automation/ConfigurationManagementAccount'
    COLLECTION_NAME = 'cmAccounts'
    PRIMARY_KEY = 'cm_account_id'

    def __init__(self, cm_account_id=None, **kwargs):
        Resource.__init__(self)
        self.__cm_account_id = cm_account_id
        self.__account_number = None
        self.__budget = None
        self.__cm_service = None
        self.__created_timestamp = None
        self.__description = None
        self.__guid = None
        self.__last_modified_timestamp = None
        self.__name = None
        self.__removable = None
        self.__status = None
        self.__customer = None
        self.__label = None
        self.__owning_groups = None

    @property
    def cm_account_id(self):
        """The unique ID of this configuration management account."""
        return self.__cm_account_id

    @lazy_property
    def account_number(self):
        """The account number that identifies you with your configuration 
        management account. This is something that will never change."""
        return self.__account_number

    @lazy_property
    def budget(self):
        """The DCM ID of the budget under which charges associated with this 
        configuration management account are billed. This is currently 
        read-only as chargebacks for configuration management are not currently 
        supported."""
        return self.__budget

    @lazy_property
    def cm_service(self):
        """The configuration management service behind this option. DCM 
        supports public services like the OpsCode Platform as well as private 
        ones visible only to the customers who own them."""
        return self.__cm_service

    @lazy_property
    def created_timestamp(self):
        """A date and time when this account was first created in DCM"""
        return self.__created_timestamp

    @lazy_property
    def description(self):
        """A description of the CM account."""
        return self.__description

    @lazy_property
    def guid(self):
        """A unique GUID that identifies the CM account."""
        return self.__guid

    @lazy_property
    def last_modified_timestamp(self):
        """A date and time when this account was last changed in DCM."""
        return self.__last_modified_timestamp

    @lazy_property
    def name(self):
        """The user-friendly name for the CM account."""
        return self.__name

    @lazy_property
    def removable(self):
        """Indicates whether or not it is safe to remove this account."""
        return self.__removable

    @lazy_property
    def status(self):
        """The current status of the CM account."""
        return self.__status

    @lazy_property
    def customer(self):
        """The customer to whom this account belongs."""
        return self.__customer

    @lazy_property
    def label(self):
        """A label assigned to this configuration management account."""
        return self.__label

    @lazy_property
    def owning_groups(self):
        """The value is currently always empty"""
        return self.__owning_groups
        
    @classmethod
    def all(cls, **kwargs):
        """List all CM accounts"""
        res = Resource(cls.PATH)
        if 'details' in kwargs:
            res.request_details = kwargs['details']
        else:
            res.request_details = 'basic'

        cma = res.get()
        if res.last_error is None:
            return [cls(i[camelize(cls.PRIMARY_KEY)]) \
            for i in cma[cls.COLLECTION_NAME]]
        else:
            raise CMException(res.last_error)

class CMException(BaseException): 
    """CM Exception"""
    pass

"""
mixcoatl.admin.account
----------------------

Implements access to the DCM Account API
"""
from mixcoatl.resource import Resource
from mixcoatl.decorators.lazy import lazy_property
from mixcoatl.utils import camelize
import json

# pylint: disable-msg=R0904,R0902
class Account(Resource):
    """An account object represents an DCM account held by a DCM customer."""

    PATH = 'admin/Account'
    COLLECTION_NAME = 'accounts'
    PRIMARY_KEY = 'account_id'

    def __init__(self, account_id = None, **kwargs):
        Resource.__init__(self)
        self.__account_id = account_id
        self.__alert_configuration = None
        self.__billing_system_id = None
        self.__cloud_subscription = None
        self.__configured = None
        self.__customer = None
        self.__default_budget = None
        self.__dns_automation = None
        self.__name = None
        self.__owner = None
        self.__plan_id = None
        self.__provisioned = None
        self.__status = None
        self.__subscribed = None

    @property
    def account_id(self):
        """`int` - The unique ID of this account"""
        return self.__account_id

    @lazy_property
    def alert_configuration(self):
        """`dict` - The configuration of alert preferences for this account."""
        return self.__alert_configuration

    @lazy_property
    def billing_system_id(self):
        """`int` - The account ID that may appear on invoices."""
        return self.__billing_system_id

    @lazy_property
    def cloud_subscription(self):
        """`dict` or `None` -- Information about the cloud for this account"""
        return self.__cloud_subscription

    @lazy_property
    def configured(self):
        """`bool` - Is this account tied to an account with a cloud provider"""
        return self.__configured

    @lazy_property
    def customer(self):
        """`dict` - The DCM customer record to which this account belongs"""
        return self.__customer

    @lazy_property
    def default_budget(self):
        """The unique billing code id for the discovered resources"""
        return self.__default_budget

    @lazy_property
    def dns_automation(self):
        """Does this account subscribe to dns_automation?"""
        return self.__dns_automation

    @lazy_property
    def name(self):
        """`str` - User-friendly name used to identify the account"""
        return self.__name

    @lazy_property
    def owner(self):
        """`dict` - user who owns this account"""
        return self.__owner

    @lazy_property
    def plan_id(self):
        """`int` - pricing plan associated with this account"""
        return self.__plan_id

    @lazy_property
    def provisioned(self):
        """`bool` - Is this account in goodstanding and managed by enStratus"""
        return self.__provisioned

    @lazy_property
    def status(self):
        """`str` - The current account payment status"""
        return self.__status

    @lazy_property
    def subscribed(self):
        """`bool` - If the account is configured and working with DCM"""
        return self.__subscribed


    @classmethod
    def all(cls, keys_only = False, **kwargs):
        """Get all accounts

        >>> Account.all(detail='basic')
        [{'account_id':12345,....}]

        >>> Account.all(keys_only=True)
        [12345]

        :param keys_only: Only return `account_id` instead of `Account` objects
        :type keys_only: bool.
        :param detail: The level of detail to return - `basic` or `extended`
        :type detail: str.
        :param cloud_id: Only show accounts tied to the given cloud
        :type cloud_id: int.
        :returns: `list` of :class:`Account` or :attr:`account_id`
        :raises: :class:`AccountException`
        """

        res = Resource(cls.PATH)
        if 'detail' in kwargs:
            res.request_details = kwargs['detail']
        else:
            res.request_details = 'basic'

        if 'cloud_id' in kwargs:
            params = {'cloudId': kwargs['cloud_id']}
        else:
            params = {}

        acc = res.get(params=params)
        if res.last_error is None:
            if keys_only is True:
                return [i[camelize(cls.PRIMARY_KEY)] for i \
                in acc[cls.COLLECTION_NAME]]
            else:
                return [cls(i[camelize(cls.PRIMARY_KEY)]) for i \
                in acc[cls.COLLECTION_NAME]]
        else:
            raise AccountException(res.last_error)
    
    def assign_cloud(self, 
                     cloud_id, 
                     account_number, 
                     api_key_id, 
                     api_key_secret):
        """ Associate this account with the cloud and supporting credentials.

        :param cloud_id: Cloud ID of the cloud that will be associated.
        :type cloud_id: int.
        :param account_number: Account number of the cloud credential.
        :type account_number: str.
        :param api_key_id: API access key of the cloud credential.
        :type api_key_id: str.
        :param api_key_secret: API secret key of the cloud credential.
        :type api_key_secret: str.
        :returns: cloud subscription ID.
        :raises: :class:`AssignCloudException`
        """

        path = "%s/%s" % (self.PATH, str(self.account_id))
        payload = {'assignCloud': {
                       'accounts': {
                           'cloudSubscription': {
                               'cloudId': cloud_id,
                               'accountNumber': account_number,
                               'apiKeyId': api_key_id,
                               'apiKeySecret': api_key_secret }}}}
        self.put(path, data=json.dumps(payload))
        if self.last_error is None:
            self.load()
            return self.cloud_subscription['cloud_subscription_id']
        else:
            raise AssignCloudException(self.last_error)

class AccountException(BaseException):
    """Account Exception"""
    pass

class AssignCloudException(AccountException):
    """Assign Cloud Exception"""
    pass

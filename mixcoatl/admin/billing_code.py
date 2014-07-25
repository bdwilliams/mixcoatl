"""
mixcoatl.admin.billing_code
---------------------------

Implements access to the DCM Billingcode API
"""
from mixcoatl.resource import Resource
from mixcoatl.decorators.lazy import lazy_property
from mixcoatl.decorators.validations import required_attrs
import json

# pylint: disable-msg=R0904,R0902
class BillingCode(Resource):
    """A billing code is a budget item with optional hard and soft quotas
    against which cloud resources may be provisioned and tracked."""

    PATH = 'admin/BillingCode'
    COLLECTION_NAME = 'billingCodes'
    PRIMARY_KEY = 'billing_code_id'

    def __init__(self, billing_code_id = None, **kwargs):
        Resource.__init__(self)
        self.__billing_code_id = billing_code_id
        self.__budget_state = None
        self.__current_usage = None
        self.__customer = None
        self.__projected_usage = None
        self.__status = None
        self.__soft_quota = None
        self.__hard_quota = None
        self.__finance_code = None
        self.__name = None
        self.__description = None

    @property
    def billing_code_id(self):
        """`int` - The unique id of this billing code"""
        return self.__billing_code_id

    @lazy_property
    def budget_state(self):
        """`str` - The ability of users to provision against this budget"""
        return self.__budget_state

    @lazy_property
    def current_usage(self):
        """`dict` - The month-to-data usage across all clouds for this code"""
        return self.__current_usage

    @lazy_property
    def customer(self):
        """`dict` - The customer to whom this code belongs"""
        return self.__customer

    @lazy_property
    def description(self):
        """`str` - User-friendly description of this code"""
        return self.__description

    @description.setter
    def description(self, description):
        """Sets the billing code description"""
        self.__description = description

    @lazy_property
    def finance_code(self):
        """`str` - The alphanumeric identifier of this billing code"""
        return self.__finance_code
    
    @finance_code.setter
    def finance_code(self, fcode):
        """Sets the billing code"""
        self.__finance_code = fcode

    @lazy_property
    def name(self):
        """`str` - User-friendly name for this billing code"""
        return self.__name

    @name.setter
    def name(self, name):
        """Sets the billing code name"""
        self.__name = name

    @lazy_property
    def projected_usage(self):
        """`dict` - Estimated end-of-month total charged against this budget"""
        return self.__projected_usage

    @lazy_property
    def status(self):
        """`str` - The status of this billing code"""
        return self.__status

    @lazy_property
    def hard_quota(self):
        """`dict` - Cutoff point where no further resources can be billed """
        return self.__hard_quota

    @hard_quota.setter
    def hard_quota(self, hquota):
        """Sets the hard quota"""
        self.__hard_quota = hquota

    @lazy_property
    def soft_quota(self):
        """`dict` - Point where budget alerts will be triggered"""
        return self.__soft_quota

    @soft_quota.setter
    def soft_quota(self, squota):
        """Sets the soft quota"""
        self.__soft_quota = squota

    @classmethod
    def all(cls, keys_only = False, **kwargs):
        """Get all visible billing codes

        .. note::

        The keys used to make the original request determine result visibility

        :param keys_only: Only return :attr:`billing_code_id` 
            instead of :class:`BillingCode` objects
        :type keys_only: bool.
        :param detail: The level of detail to return - `basic` or `extended`
        :type detail: str.
        :returns: `list` - of :class:`BillingCode` or :attr:`billing_code_id`
        :raises: :class:`BillingCodeException`
        """
        res = Resource(cls.PATH)
        if 'details' in kwargs:
            res.request_details = kwargs['details']
        else:
            res.request_details = 'basic'

        bcs = res.get()
        if res.last_error is None:
            if keys_only is True:
                return [i['billingCodeId'] for i in bcs[cls.COLLECTION_NAME]]
            else:
                return [cls(i['billingCodeId']) \
                for i in bcs[cls.COLLECTION_NAME]]
        else:
            raise BillingCodeException(res.last_error)

    @required_attrs(['soft_quota',
                    'hard_quota',
                    'name',
                    'finance_code',
                    'description'])
    def add(self):
        """Add a new billing code. """

        payload = {"addBillingCode":[{
                   "softQuota": {"value": self.soft_quota, "currency": "USD"},
                   "hardQuota": {"value": self.hard_quota, "currency": "USD"},
                   "status": "ACTIVE",
                   "name": self.name,
                   "financeCode": self.finance_code,
                   "description": self.description}]}
        response = self.post(data=json.dumps(payload))
        if self.last_error is None:
            return response
        else:
            raise BillingCodeAddException(self.last_error)

    @required_attrs(['billing_code_id'])
    def destroy(self, reason, replacement_code):
        """Destroy billing code with a specified reason :attr:`reason`

        :param reason: The reason of destroying the billing code.
        :type reason: str.
        :param replacement_code: The replacement code.
        :type replacement_code: int.
        :returns: bool -- Result of API call
        """
        path = self.PATH+"/"+str(self.billing_code_id)
        qopts = {'reason':reason, 'replacementCode':replacement_code}
        self.delete(path, params=qopts)
        if self.last_error is None:
            return True
        else:
            raise BillingCodeDestroyException(self.last_error)

class BillingCodeException(BaseException): 
    """Billing Code Exception"""
    pass

class BillingCodeAddException(BillingCodeException): 
    """Billing Code Add Exception"""
    pass

class BillingCodeDestroyException(BillingCodeException):
    """Billing Code Destroy Exception"""
    pass

"""
mixcoatl.admin.user
-------------------

Implements access to the DCM User API
"""
from mixcoatl.resource import Resource
from mixcoatl.decorators.lazy import lazy_property
from mixcoatl.decorators.validations import required_attrs
from mixcoatl.utils import camel_keys
import json

# pylint: disable-msg=R0902,R0904
class User(Resource):
    """A user within the DCM environment"""

    PATH = 'admin/User'
    COLLECTION_NAME = 'users'
    PRIMARY_KEY = 'user_id'

    def __init__(self, user_id=None, **kwargs):
        Resource.__init__(self)
        self.__user_id = user_id
        self.__account_user_id = None
        self.__alpha_name = None
        self.__cloud_console_password = None
        self.__cloud_api_public_key = None
        self.__cloud_api_secret_key = None
        self.__customer = None
        self.__editable = None
        self.__has_cloud_api_access = None
        self.__has_cloud_console_access = None
        self.__legacy_user_id = None
        self.__notification_targets = None
        self.__notification_settings = None
        self.__status = None
        self.__time_zone = None
        self.__vm_login_id = None
        self.__ssh_public_key = None
        self.__password = None

    @property
    def user_id(self):
        """`int` The DCM unique id of this user across all customer accounts"""
        return self.__user_id

    @lazy_property
    def account(self):
        """`dict` The DCM account"""
        return self.__account

    @account.setter
    def account(self, account):
        """Sets the DCM account"""
        # pylint: disable-msg=C0111,W0201
        self.__account = account

    @lazy_property
    def account_user_id(self):
        """`str` or `None` A unique identifier to reference this user's access
            to a specific account
        """
        return self.__account_user_id

    @lazy_property
    def alpha_name(self):
        """`str` The user's full name in the form of `Last name, First name`"""
        return self.__alpha_name

    @lazy_property
    def billing_codes(self):
        """`list` The billing codes against which this user has rights

        .. note::

            Only when this user is queried in the context of `account_id`

        """
        return self.__billing_codes

    @billing_codes.setter
    def billing_codes(self, bcode):
        """Sets the billing code."""
        # pylint: disable-msg=C0111,W0201
        self.__billing_codes = bcode

    @lazy_property
    def cloud_console_password(self):
        """`str` The encrypted password the user logs into the cloud with"""
        return self.__cloud_console_password

    @lazy_property
    def cloud_api_public_key(self):
        """`str` The encrypted public key the user makes API calls to the 
        underlying cloud with"""
        return self.__cloud_api_public_key

    @lazy_property
    def cloud_api_secret_key(self):
        """`str` The encrypted secret key the user can make API calls to 
        the underlying cloud with"""
        return self.__cloud_api_secret_key

    @lazy_property
    def customer(self):
        """`dict` The customer record to which this user belongs"""
        return self.__customer

    @lazy_property
    def editable(self):
        """`bool` Indicates if the core values of this user may be changed"""
        return self.__editable

    @lazy_property
    def email(self):
        """`str` Email is a unique identifier that enables a given user to
            identify themselves to DCM
        """
        return self.__email

    @email.setter
    def email(self, email):
        """Sets the email."""
        # pylint: disable-msg=C0111,W0201
        self.__email = email

    @lazy_property
    def family_name(self):
        """`str` The family name of the user"""
        return self.__family_name

    @family_name.setter
    def family_name(self, famname):
        """Sets the family name."""
        # pylint: disable-msg=C0111,W0201
        self.__family_name = famname

    @lazy_property
    def given_name(self):
        """`str` The given name of the user"""
        return self.__given_name

    @given_name.setter
    def given_name(self, gname):
        """Sets the given name."""
        # pylint: disable-msg=C0111,W0201
        self.__given_name = gname

    @lazy_property
    def groups(self):
        """`list` The group membership of this user idependent of any 
        individual accounts"""
        return self.__groups

    @groups.setter
    def groups(self, group):
        """Sets the group name."""
        # pylint: disable-msg=C0111,W0201
        self.__groups = group

    @lazy_property
    def has_cloud_api_access(self):
        """`bool` Indicates that the user has access to the underlying 
        cloud API (i.e. AWS IAM)"""
        return self.__has_cloud_api_access

    @lazy_property
    def has_cloud_console_access(self):
        """`bool` Indicates that the user has access to the underlying 
        cloud console (i.e. AWS IAM)"""
        return self.__has_cloud_console_access

    @lazy_property
    def legacy_user_id(self):
        """`int` The legacy user id"""
        return self.__legacy_user_id

    @lazy_property
    def notifications_targets(self):
        """`dict` The various targets configured for delivery of 
        notifications"""
        return self.__notification_targets

    @lazy_property
    def notifications_settings(self):
        """`dict` Notification settings configured for this user"""
        return self.__notification_settings

    @lazy_property
    def status(self):
        """`str` The current status of this user in DCM"""
        return self.__status

    @lazy_property
    def time_zone(self):
        """`str` The timezone id for the user's prefered time zone"""
        return self.__time_zone

    @lazy_property
    def vm_login_id(self):
        """`str` The username the user will use to login to cloud instances
            for shell or remote desktop access
        """
        return self.__vm_login_id

    @lazy_property
    def ssh_public_key(self):
        """`str` The public key to grant the user access to Unix instances"""
        return self.__ssh_public_key

    @lazy_property
    def password(self):
        """`str` DCM login password"""
        return self.__password

    @password.setter
    def password(self, password):
        """Sets the password."""
        self.__password = password

    @required_attrs(['user_id'])
    def grant(self, account_id, groups, billing_codes):
        """Grants the user access to the specified account. :attr:`reason`

        :param account_id: Account ID of the account to grant access.
        :type account_id: int.
        :param groups: List of group ID the user will belong to.
        :type groups: list.
        :param billing_codes: List of billing code the user will use.
        :type billing_codes: list.
        :returns: bool -- Result of API call
        """
        path = '%s/%s' % (self.PATH, str(self.user_id))

        group_list = []
        billing_code_list = []
        for group in groups:
            group_list.append({"groupId": group})
        for billing_code in billing_codes:
            billing_code_list.append({"billingCodeId": billing_code})

        payload = {"grant":[{"account": {"accountId": account_id},
                             "groups": group_list,
                             "billingCodes": billing_code_list}]}

        return self.put(path, data=json.dumps(payload))

    @required_attrs(['account', 
                    'given_name', 
                    'family_name', 
                    'email', 
                    'groups', 
                    'billing_codes'])
    def create(self):
        """Creates a new user."""

        billing_code_list = []
        for billing_code in self.billing_codes:
            billing_code_list.append({"billingCodeId": billing_code})

        parms = [{'givenName':self.given_name,
                  'familyName': self.family_name,
                  'email': self.email,
                  'groups': [{'groupId':self.groups}],
                  'account': {'accountId':self.account},
                  'billingCodes': billing_code_list}]

        if self.password is not None:
            parms[0].update({'password': self.password})

        payload = {'addUser':camel_keys(parms)}

        response = self.post(data=json.dumps(payload))
        if self.last_error is None:
            self.load()
            return response
        else:
            raise UserCreationException(self.last_error)

    @classmethod
    def all(cls, keys_only=False, **kwargs):
        """Return all users

        .. note::

            The keys used to make the request determine results visibility

        :param keys_only: Return :attr:`user_id` instead of :class:`User`
        :type keys_only: bool.
        :param detail: str. The level of detail to return - `basic` 
            or `extended`
        :type detail: str.
        :returns: `list` of :class:`User` or :attr:`user_id`
        :raises: :class:`UserException`
        """
        res = Resource(cls.PATH)
        if 'detail' in kwargs:
            res.request_details = kwargs['detail']
        else:
            res.request_details = 'basic'

        users = res.get()
        if res.last_error is None:
            if keys_only is True:
                return [i['userId'] for i in users[cls.COLLECTION_NAME]]
            else:
                return [cls(i['userId']) for i in users[cls.COLLECTION_NAME]]
        else:
            raise UserException(res.last_error)

class UserException(BaseException):
    """User Exception"""
    pass

class UserCreationException(UserException):
    """User Creation Exception"""
    pass

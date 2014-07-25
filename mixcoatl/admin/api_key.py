"""
mixcoatl.admin.api_key
----------------------

Implements access to the DCM ApiKey API
"""
from mixcoatl.resource import Resource
from mixcoatl.decorators.lazy import lazy_property
from mixcoatl.decorators.validations import required_attrs
import json

# pylint: disable-msg=R0904,R0902
class ApiKey(Resource):
    """An API key is an access key & secret key that provide access DCM."""

    PATH = 'admin/ApiKey'
    COLLECTION_NAME = 'apiKeys'
    PRIMARY_KEY = 'access_key'

    def __init__(self, access_key = None, **kwargs):
        Resource.__init__(self)
        self.__access_key = access_key
        self.__account = None
        self.__activation = None
        self.__customer = None
        self.__customer_management_key = None
        self.__state = None
        self.__user = None
        self.__name = None
        self.__description = None
        self.__expiration = None
        self.__secret_key = None
        self.__system_management_key = None
        self.description = None
        self.name = None

    @property
    def access_key(self):
        """The primary identifier of the `ApiKey`. Same as `ES_ACCESS_KEY`"""
        return self.__access_key

    @lazy_property
    def account(self):
        """`dict` - The account with which this API key is associated."""
        return self.__account

    @lazy_property
    def activation(self):
        """`str` - The date and time when this key was activated."""
        return self.__activation

    @lazy_property
    def expiration(self):
        """`str` - The date when the API key should become deactivatate."""
        return self.__expiration

    @expiration.setter
    def expiration(self, expiration):
        """Sets the date in which the API key should deactivate"""
        self.__expiration = expiration

    @lazy_property
    def customer(self):
        """`dict` - The customer to whom this API key belongs."""
        return self.__customer

    @lazy_property
    def customer_management_key(self):
        """`bool` - Identifies whether or not this key can be used across all 
        customer accounts."""
        return self.__customer_management_key

    # @lazy_property
    # def description(self):
    #     """`str` - A user-friendly description of this API key."""
    #     return self.__description

    # @description.setter
    # def description(self, description):
    #     """Sets the API key description."""
    #     self.__description = description

    # @lazy_property
    # def name(self):
    #     """`str` - The user-friendly name used to identify the key."""
    #     return self.__name

    # @name.setter
    # def name(self, name):
    #     """Sets the name to identify the key."""
    #     self.__name = name

    @lazy_property
    def secret_key(self):
        """`str` - The secret part of this API key."""
        return self.__secret_key

    @lazy_property
    def state(self):
        """`str` - The status of the key *(i.e. `ACTIVE`)*"""
        return self.__state

    @lazy_property
    def system_management_key(self):
        """`bool` - Identifies if the key can be used for DCM system 
        management functions"""
        return self.__system_management_key

    @system_management_key.setter
    def system_management_key(self, system_management_key):
        """DCM System Management Key."""
        self.__system_management_key = system_management_key

    @lazy_property
    def user(self):
        """`dict` - The user associated with this API key. 
        Account-level keys return `{'user_id': -1}`"""
        return self.__user

    @required_attrs(['description', 'name'])
    def create(self):
        """Call the API to generate an API key from the current 
        instance of `ApiKey`"""

        payload = {'generateApiKey':[{'description':self.description, 
        'name':self.name}]}
        svr = self.post(data=json.dumps(payload))
        if self.last_error is None:
            self.__access_key = svr['apiKeys'][0]['accessKey']
            self.load()
        else:
            raise ApiKeyGenerationException(self.last_error)

    def invalidate(self, reason='key deleted via mixcoatl'):
        """Call the API to invalidate the current instance of `ApiKey`
        This is the same as deleting the api key

        :param reason: the reason for invalidating the key
        :type reason: str.
        :returns: True
        :raises: :class:`ApiKeyInvalidationException`
        """
        params = {'reason': reason}
        self.delete(params=params)
        if self.last_error is None:
            return True
        else:
            raise ApiKeyInvalidationException(self.last_error)

    @classmethod
    def generate_api_key(cls, key_name, description):
        """Generates a new API key

        >>> ApiKey.generate_api_key('my-api-key', 'this is my api key')
        {'access_key':'ABCDEFGHIJKL':....}

        :param key_name: the name for the key
        :type key_name: str.
        :param description: the description for the key
        :type description: str.
        :param expiration: *unused for now*
        :type expiration: str.
        :returns: :class:`ApiKey`
        :raises: :class:`ApiKeyGenerationException`
        """

        api = cls()
        api.name = key_name
        api.description = description
        api.create()
        return api

    @classmethod
    def all(cls, keys_only=False, **kwargs):
        """Get all api keys

        .. note::

            The keys used to make the request determine results visibility

        :param keys_only: Only return `access_key` instead of `ApiKey` objects
        :type keys_only: bool.
        :param detail: The level of detail to return - `basic` or `extended`
        :type detail: str.
        :param account_id: Display all system keys belonging to `account_id`
        :type account_id: int.
        :param user_id: Display all keys belonging to `user_id`
        :type user_id: int.
        :returns: `list` - of :class:`ApiKey` or :attr:`access_key`
        """

        res = Resource(cls.PATH)
        if 'detail' in kwargs:
            res.request_details = kwargs['detail']
        else:
            res.request_details = 'basic'

        if 'account_id' in kwargs:
            params = {'accountId': kwargs['account_id']}
        elif 'user_id' in kwargs:
            params = {'userId': kwargs['user_id']}
        else:
            params = {}

        col = res.get(params=params)
        if res.last_error is None:
            if keys_only is True:
                return [i['accessKey'] for i in col[cls.COLLECTION_NAME]]
            else:
                return [cls(i['accessKey']) for i in col[cls.COLLECTION_NAME]]
        else:
            raise ApiKeyException(res.last_error)

class ApiKeyException(BaseException): 
    """API Key Exception"""
    pass

class ApiKeyGenerationException(ApiKeyException): 
    """API Key Generation Exception"""
    pass

class ApiKeyInvalidationException(ApiKeyException): 
    """API Key Invalidation Exception"""
    pass

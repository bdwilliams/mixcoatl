"""
mixcoatl.admin.role
--------------------

Implements access to the DCM Role API

"""
from mixcoatl.resource import Resource
from mixcoatl.decorators.lazy import lazy_property
from mixcoatl.decorators.validations import required_attrs
from mixcoatl.utils import camel_keys

import json

# pylint: disable-msg=R0902,R0904
class Role(Resource):
    """A role defines a common set of permissions that govern access into a 
    given account"""

    PATH = 'admin/Role'
    COLLECTION_NAME = 'roles'
    PRIMARY_KEY = 'role_id'

    def __init__(self, role_id=None, **kwargs):
        Resource.__init__(self)
        self.__role_id = role_id
        self.__acl = None
        self.__status = None
        self.__customer = None

    @property
    def role_id(self):
        """`int` - The unique id of the role"""
        return self.__role_id

    @lazy_property
    def acl(self):
        """`dict` - The access permissions associated with the role"""
        return self.__acl

    @acl.setter
    def acl(self, acl):
        """Sets access permissions for the role."""
        self.__acl = acl

    @lazy_property
    def description(self):
        """`str` - A user-friendly description of the role"""
        return self.__description

    @description.setter
    def description(self, desc):
        """Sets the name of the description."""
        # pylint: disable-msg=C0111,W0201
        self.__description = desc

    @lazy_property
    def customer(self):
        """`dict` - The customer to whom this role belongs"""
        return self.__customer

    @customer.setter
    def customer(self, customer):
        """Sets the customer of the role."""
        self.__customer = customer

    @lazy_property
    def name(self):
        """`str` - The name of the role"""
        return self.__name

    @name.setter
    def name(self, desc):
        """Sets the name of the role."""
        # pylint: disable-msg=C0111,W0201
        self.__name = desc

    @lazy_property
    def status(self):
        """`str` - The status of the role in DCM"""
        return self.__status

    @status.setter
    def status(self, status):
        """Sets the status of the role."""
        self.__status = status

    @required_attrs(['role_id'])
    def grant(self, role_id, resource_type, action, qualifier):
        """Adds a new ACL to a role."""

        parms = [{'acl': [{'resourceType' : resource_type,
                    'action' : action,
                    'qualifier' : qualifier}]}]

        path = '%s/%s' % (self.PATH, str(role_id))

        payload = {'grant':camel_keys(parms)}

        response = self.put(path, data=json.dumps(payload))
        if self.last_error is None:
            self.load()
            return response
        else:
            raise SetACLException(self.last_error)

    @required_attrs(['name', 'description'])
    def create(self):
        """Creates a new role. Status is hard-coded to ACTIVE for now. """

        parms = [{'status': "ACTIVE",
                    'name':self.name,
                    'description': self.description}]

        payload = {'addRole':camel_keys(parms)}

        response = self.post(data=json.dumps(payload))
        if self.last_error is None:
            self.load()
            return response
        else:
            raise RoleCreationException(self.last_error)

    @classmethod
    def all(cls, keys_only = False, **kwargs):
        """Get all roles

        .. note::

            The keys used to make the request determine results visibility

        :param keys_only: Only return :attr:`role_id` 
            instead of :class:`Group` objects
        :type keys_only: bool.
        :param detail: The level of detail to return - `basic` or `extended`
        :type detail: str.
        :param account_id: List roles with mappings to groups in the 
            specified account
        :type account_id: int.
        :param group_id: Provides the role associated with the specified group
        :type group_id: int.
        :returns: `list` of :attr:`role_id` or :class:`Role`
        :raises: :class:`RoleException`
        """
        res = Resource(cls.PATH)
        params = {}
        if 'detail' in kwargs:
            res.request_details = kwargs['detail']
        else:
            res.request_details = 'basic'

        if 'account_id' in kwargs:
            params['account_id'] = kwargs['account_id']

        if 'group_id' in kwargs:
            params['group_id'] = kwargs['group_id']

        roles = res.get(params=params)
        if res.last_error is None:
            if keys_only is True:
                return [i['roleId'] for i in roles[cls.COLLECTION_NAME]]
            else:
                return [cls(i['roleId']) for i in roles[cls.COLLECTION_NAME]]
        else:
            raise RoleException(res.last_error)

class RoleException(BaseException): 
    """Role Exception"""
    pass

class SetACLException(RoleException):
    """Role Creation Exception"""
    pass

class RoleCreationException(RoleException):
    """Role Creation Exception"""
    pass

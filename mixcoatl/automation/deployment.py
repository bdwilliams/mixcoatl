"""Implements the DCM Deployment API"""
from mixcoatl.resource import Resource
from mixcoatl.decorators.lazy import lazy_property
from mixcoatl.decorators.validations import required_attrs
from mixcoatl.utils import camelize, camel_keys

import json

# pylint: disable-msg=R0902,R0904
class Deployment(Resource):
    """A deployment is the central concept in the DCM automation system. It 
    represents a logical system made up of multiple tiers that may be spread 
    across multiple clouds. The deployment and its components capture the rules 
    around which your system should be automated in DCM."""
    PATH = 'automation/Deployment'
    COLLECTION_NAME = 'deployments'
    PRIMARY_KEY = 'deployment_id'

    def __init__(self, deployment_id=None, **kwargs):
        Resource.__init__(self)
        self.__deployment_id = deployment_id
        self.__backup_window = None
        self.__label = None
        self.__creation_timestamp = None
        self.__customer = None
        self.__for_service_catalog = None
        self.__launch_timestamp = None
        self.__maintenance_window = None
        self.__owning_groups = None
        self.__owning_user = None
        self.__removable = None
        self.__load_balancers = None
        self.__reason_not_removable = None
        self.__status = None
        self.__e_type = None
        self.__dr_storage = None
        self.region = None

    @property
    def deployment_id(self):
        """The Unique ID for this deployment."""
        return self.__deployment_id

    @lazy_property
    def backup_window(self):
        """The time window during which any daily backups may be performed."""
        return self.__backup_window

    @lazy_property
    def budget(self):
        """ID of the default billing code."""
        return self.__budget

    @budget.setter
    def budget(self, budget):
        """Sets the budget."""
        # pylint: disable-msg=C0111,W0201
        self.__budget = budget

    @lazy_property
    def label(self):
        """The label assigned to the deployment."""
        return self.__label

    @lazy_property
    def creation_timestamp(self):
        """The date and time when this deployment was first created."""
        return self.__creation_timestamp

    @lazy_property
    def customer(self):
        """The customer in whose library this deployment is being managed."""
        return self.__customer

    @lazy_property
    def description(self):
        """Full description of the deployment."""
        return self.__description

    @description.setter
    def description(self, desc):
        """Sets the description."""
        # pylint: disable-msg=C0111,W0201
        self.__description = desc

    @lazy_property
    def for_service_catalog(self):
        """Return or exclude deployments based on their service catalog 
        status."""
        return self.__for_service_catalog

    @lazy_property
    def launch_timestamp(self):
        """If currently running or in maintenance, this value is the date and 
        time when the deployment was initially launched"""
        return self.__launch_timestamp

    @lazy_property
    def maintenance_window(self):
        """The time window during which DCM performs automated maintenance such 
        as patching servers and rolling out deployment changes."""
        return self.__maintenance_window

    @lazy_property
    def name(self):
        """The deployment name."""
        return self.__name

    @name.setter
    def name(self, name):
        """Sets the name."""
        # pylint: disable-msg=C0111,W0201
        self.__name = name

    @lazy_property
    def owning_groups(self):
        """The groups who have ownership over this deployment."""
        return self.__owning_groups

    @lazy_property
    def owning_user(self):
        """The user who is the owner of record of this deployment."""
        return self.__owning_user

    @lazy_property
    def regions(self):
        """Lists the set of regions for which this deployment is currently 
        configured."""
        return self.__regions

    @regions.setter
    def regions(self, region):
        """Sets the region."""
        # pylint: disable-msg=C0111,W0201
        self.__regions = region

    @lazy_property
    def removable(self):
        """Indicates whether or not this machine image is in a state that will 
        allow you to execute a DELETE operation on it."""
        return self.__removable

    @lazy_property
    def load_balancers(self):
        """A deployment has zero or more load balancers assigned to a pool 
        from which services in the deployment can be load balanced."""
        return self.__load_balancers

    @lazy_property
    def reason_not_removable(self):
        """If the deployment isn’t currently removable, this value contains 
        an explanation for why it isn’t removable."""
        return self.__reason_not_removable

    @lazy_property
    def status(self):
        """The current status of the deployment."""
        return self.__status

    @lazy_property
    def e_type(self):
        """Indicates whether this deployment is dedicated to a single use or 
        shared among multiple uses (and thus budgets)."""
        return self.__e_type

    @lazy_property
    def dr_storage(self):
        """When set, DCM automatically copies all backups for this 
        deployment into the cloud storage associated with the target region."""
        return self.__dr_storage

    @classmethod
    def all(cls, **kwargs):
        """List all Deployments."""
        res = Resource(cls.PATH)
        if 'details' in kwargs:
            res.request_details = kwargs['details']
        else:
            res.request_details = 'basic'

        deps = res.get()
        if res.last_error is None:
            return [cls(i[camelize(cls.PRIMARY_KEY)]) \
            for i in deps[cls.COLLECTION_NAME]]
        else:
            return res.last_error

    @required_attrs(['name', 'description','budget','region'])
    def create(self):
        """Creates a new deployment

        :raises: :class:`DeploymentCreationException`
        """

        parms = [{'budget': self.budget,
                    'regionId': self.region,
                    'description': self.description,
										'name': self.name}]


        payload = {'addDeployment':camel_keys(parms)}

        response = self.post(data=json.dumps(payload))
        if self.last_error is None:
            self.load()
            return response
        else:
            raise DeploymentCreationException(self.last_error)

class DeploymentException(BaseException): 
    """Deployment Exception"""
    pass

class DeploymentCreationException(DeploymentException):
    """Deployment Creation Exception"""
    pass

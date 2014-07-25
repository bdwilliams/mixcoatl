"""
mixcoatl.network.load_balancer
--------------------
"""
from mixcoatl.resource import Resource
from mixcoatl.decorators.lazy import lazy_property
from mixcoatl.utils import camelize

# pylint: disable-msg=R0902,R0904
class LoadBalancer(Resource):
    """A load balancer is a virtual load balancer such as an AWS Elastic Load 
    Balancer. It is specifically not a VM-hosted load balancer. Load balancers
    vary wildly from cloud provider to cloud provider. As a result, you should
    check with your cloud meta-data to see what elements are necessary in order
    to create a load balancer"""
    PATH = 'network/LoadBalancer'
    COLLECTION_NAME = 'loadBalancers'
    PRIMARY_KEY = 'load_balancer_id'

    def __init__(self, load_balancer_id=None, **kwargs):
        Resource.__init__(self)
        self.__load_balancer_id = load_balancer_id
        self.__customer = None
        self.__status = None
        self.__provider_id = None
        self.__description = None
        self.__region = None
        self.__budget = None
        self.__owning_groups = None
        self.__cname_based = None
        self.__owning_groups = None
        self.__owning_account = None
        self.__owning_user = None
        self.__address = None
        self.__cloud = None
        self.__name = None
        self.__data_centers = None
        self.__servers = None
        self.__listeners = None

    @property
    def load_balancer_id(self):
        """The unique DCM ID for this load balancer."""
        return self.__load_balancer_id

    @lazy_property
    def customer(self):
        """The customer to which the load balancer belongs."""
        return self.__customer

    @lazy_property
    def status(self):
        """The current status of the load balancer."""
        return self.__status

    @lazy_property
    def provider_id(self):
        """The unique ID with the cloud provider for this load balancer."""
        return self.__provider_id

    @lazy_property
    def description(self):
        """The description of the load balancer established in DCM."""
        return self.__description

    @lazy_property
    def region(self):
        """The region in which this load balancer operates."""
        return self.__region

    @lazy_property
    def budget(self):
        """The ID of the billing code against which any costs associated with 
        this load balancer are billed."""
        return self.__budget

    @lazy_property
    def owning_groups(self):
        """The groups who have ownership over this load balancer. """
        return self.__owning_groups

    @lazy_property
    def cname_based(self):
        """Indicates whether this load balancer uses a CNAME for mapping to its
        destination."""
        return self.__cname_based

    @lazy_property
    def address(self):
        """An IPv4 or DNS address (depending on whether the load balancer is 
        CNAME based) for the load balancer."""
        return self.__address

    @lazy_property
    def owning_account(self):
        """The DCM account under which the load balancer is registered."""
        return self.__owning_account

    @lazy_property
    def owning_user(self):
        """The user who is the owner of record of this load balancer. The owner
        may be null in cases of auto-discovery or certain automated 
        scenarios."""
        return self.__owning_user

    @lazy_property
    def cloud(self):
        """The cloud in which this load balancer operates."""
        return self.__cloud

    @lazy_property
    def name(self):
        """A user-friendly name for the load balancer."""
        return self.__name

    @lazy_property
    def data_centers(self):
        """The list of data centers across which this load balancer expects to
        see endpoints."""
        return self.__data_centers

    @lazy_property
    def servers(self):
        """The list of servers in the load balancer pool. Only provided when
        detail level is EXTENDED."""
        return self.__servers

    @lazy_property
    def listeners(self):
        """The list of network services being routed through this load 
        balancer."""
        return self.__listeners

    @classmethod
    def all(cls, **kwargs):
        """List the load balancers."""
        res = Resource(cls.PATH)
        if 'details' in kwargs:
            res.request_details = kwargs['details']
        else:
            res.request_details = 'basic'

        lbs = res.get()
        if res.last_error is None:
            return [cls(i[camelize(cls.PRIMARY_KEY)]) \
            for i in lbs[cls.COLLECTION_NAME]]
        else:
            return res.last_error

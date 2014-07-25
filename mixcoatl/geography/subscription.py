"""
mixcoatl.geograpy.subscription
--------------------
"""
from mixcoatl.resource import Resource

class Subscription(Resource):
    """A subscription describes the capabilities of a specific region as 
    matched by your subscription to the region."""
    PATH = 'geography/Subscription'
    COLLECTION_NAME = 'subscriptions'
    PRIMARY_KEY = 'region_id'

    def __init__(self, region_id = None):
        Resource.__init__(self)
        self.__region_id = region_id

    @property
    def region_id(self):
        """The unique DCM ID for this region."""
        return self.__region_id

    @classmethod
    def region(cls, region_id):
        """Returns subscription for given Region"""
        res = Resource(cls.PATH+"/"+str(region_id))
        res.request_details = 'basic'
        get_data = res.get()
        return get_data

    @classmethod
    def all(cls):
        """Returns subscriptions for all regions"""
        res = Resource(cls.PATH)
        res.request_details = 'basic'
        get_data = res.get()
        return get_data
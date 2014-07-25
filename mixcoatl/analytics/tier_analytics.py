"""
mixcoatl.analytics.tier_analytics
--------------------

Implements access to the DCM Analytics API

"""
from mixcoatl.resource import Resource
from mixcoatl.decorators.lazy import lazy_property
from mixcoatl.utils import camelize

# pylint: disable-msg=R0902,R0904
class TierAnalytics(Resource):
    """Tier analytics represent the performance of a servers grouped into a 
    deployment tier over a specified period of time. A tier analytics object 
    defines a period start, end, and data capture interval and then provides 
    data points in support for those parameters."""
    PATH = 'analytics/TierAnalytics'
    COLLECTION_NAME = 'analytics'
    PRIMARY_KEY = 'tier_id'

    def __init__(self, tier_id=None, **kwargs):
        Resource.__init__(self)
        self.__tier_id = tier_id
        self.__data_points = None
        self.__period_start = None
        self.__period_end = None
        self.__interval_in_minutes = None

    @property
    def tier_id(self):
        """The unique ID for the tier represented by the analytics object."""
        return self.__tier_id

    @lazy_property
    def data_points(self):
        """Data points representing a snapshot of the tier’s state at a given
        interval point."""
        return self.__data_points

    @lazy_property
    def period_start(self):
        """The actual date and time when the data set begins"""
        return self.__period_start

    @lazy_property
    def period_end(self):
        """The actual date and time when the data set ends"""
        return self.__period_end

    @lazy_property
    def interval_in_minutes(self):
        """The interval between data points in minutes delivered by 
        this response."""
        return self.__interval_in_minutes

    @interval_in_minutes.setter
    def interval_in_minutes(self, iim):
        """Sets the interval in minutes."""
        self.__interval_in_minutes = iim

    @classmethod
    def all(cls, tier_id, **kwargs):
        """Returns analytics for the specified tier_id"""
        res = Resource(cls.PATH+'/'+str(tier_id))
        if 'details' in kwargs:
            res.request_details = kwargs['details']
        else:
            res.request_details = 'basic'

        tiers = res.get()
        if res.last_error is None:
            return [cls(i[camelize(cls.PRIMARY_KEY)]) \
            for i in tiers[cls.COLLECTION_NAME]]
        else:
            return res.last_error

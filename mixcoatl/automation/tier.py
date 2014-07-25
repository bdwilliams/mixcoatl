"""
mixcoatl.automation.tier
--------------------
"""
from mixcoatl.resource import Resource
from mixcoatl.decorators.lazy import lazy_property
from mixcoatl.decorators.validations import required_attrs
from mixcoatl.utils import camelize, camel_keys

import json

# pylint: disable-msg=R0902,R0904
class Tier(Resource):
    """A tier (formerly known as a server group) is a logical tier in a 
    deployment representing a group of servers that all handle the same 
    processing and scale up or down together."""
    PATH = 'automation/Tier'
    COLLECTION_NAME = 'tiers'
    PRIMARY_KEY = 'tier_id'

    def __init__(self, tier_id=None, **kwargs):
        Resource.__init__(self)
        self.__tier_id = tier_id
        self.__last_breach_change_timestamp = None
        self.__removable = None
        self.__scaling_rules = None
        self.__status = None
        self.__lower_cpu_threshold = None
        self.__lower_ram_threshold = None
        self.__upper_cpu_threshold = None
        self.__upper_ram_threshold = None
        self.__maximum_servers = None
        self.__budget = None
        self.__name = None
        self.__label = None
        self.__minimum_servers = None
        self.__breach_period_in_minutes = None
        self.__cooldown_period_in_minutes = None
        self.__description = None
        self.__deployment = None
        self.__breach_increment = None

    @property
    def tier_id(self):
        """The unique DCM ID for this tier."""
        return self.__tier_id

    @lazy_property
    def budget(self):
        """Budget assigned to the tier."""
        return self.__budget

    @budget.setter
    def budget(self, budget):
        """Sets the budget."""
        self.__budget = budget

    @lazy_property
    def breach_increment(self):
        """How many servers will be launched or terminated when DCM executes
        an auto-scaling event."""
        return self.__breach_increment

    @breach_increment.setter
    def breach_increment(self, breach):
        """Sets the breach increment."""
        self.__breach_increment = breach

    @lazy_property
    def breach_period_in_minutes(self):
        """The number of minutes that must pass after a breach threshold has 
        been crossed before DCM executes an auto-scaling event."""
        return self.__breach_period_in_minutes

    @breach_period_in_minutes.setter
    def breach_period_in_minutes(self, breach):
        """Sets breach period."""
        self.__breach_period_in_minutes = breach

    @lazy_property
    def cooldown_period_in_minutes(self):
        """The number of minutes that must pass after an auto-scaling event 
        before DCM begins checking for auto-scaling threshold breaches."""
        return self.__cooldown_period_in_minutes

    @cooldown_period_in_minutes.setter
    def cooldown_period_in_minutes(self, cooldown):
        """Sets cooldown period."""
        self.__cooldown_period_in_minutes = cooldown

    @lazy_property
    def deployment(self):
        """Returns the tiers belonging to the deployment with the specified 
        unique ID."""
        return self.__deployment

    @deployment.setter
    def deployment(self, deployment):
        """Sets the deployment."""
        self.__deployment = deployment

    @lazy_property
    def label(self):
        """A label assigned to this deployment."""
        return self.__label

    @label.setter
    def label(self, label):
        """Sets the label."""
        self.__label = label

    @lazy_property
    def description(self):
        """The full description of the deployment."""
        return self.__description

    @description.setter
    def description(self, desc):
        """Sets the description."""
        self.__description = desc

    @lazy_property
    def last_breach_change_timestamp(self):
        """The date and time when this tier last changed its status."""
        return self.__last_breach_change_timestamp

    @lazy_property
    def lower_cpu_threshold(self):
        """A number between 1 and 100 representing the percentage of CPU for 
        the lower CPU threshold."""
        return self.__lower_cpu_threshold

    @lower_cpu_threshold.setter
    def lower_cpu_threshold(self, cpu):
        """Sets the lower cpu."""
        self.__lower_cpu_threshold = cpu

    @lazy_property
    def lower_ram_threshold(self):
        """A number between 1 and 100 representing the percentage of RAM for 
        the lower RAM threshold."""
        return self.__lower_ram_threshold

    @lower_ram_threshold.setter
    def lower_ram_threshold(self, ram):
        """Sets lower ram."""
        self.__lower_ram_threshold = ram

    @lazy_property
    def minimum_servers(self):
        """The minimum number of servers allowed to be active in this tier."""
        return self.__minimum_servers

    @minimum_servers.setter
    def minimum_servers(self, minimum):
        """Sets minimum servers."""
        self.__minimum_servers = minimum

    @lazy_property
    def maximum_servers(self):
        """The maximum number of servers allowed to be active in this tier."""
        return self.__maximum_servers

    @maximum_servers.setter
    def maximum_servers(self, maximum):
        """Sets maximum servers."""
        self.__maximum_servers = maximum

    @lazy_property
    def name(self):
        """A user-friendly name for the deployment."""
        return self.__name

    @name.setter
    def name(self, name):
        """Sets the name."""
        self.__name = name

    @lazy_property
    def removable(self):
        """Indicates whether or not this tier is in a state that will allow 
        you to execute a DELETE operation on it."""
        return self.__removable

    @lazy_property
    def scaling_rules(self):
        """The scaling rules you want to use for scaling this tier."""
        return self.__scaling_rules

    @lazy_property
    def status(self):
        """The current status of the tier."""
        return self.__status

    @lazy_property
    def upper_cpu_threshold(self):
        """A number between 1 and 100 representing the percentage of CPU for 
        the upper CPU threshold."""
        return self.__upper_cpu_threshold

    @upper_cpu_threshold.setter
    def upper_cpu_threshold(self, upper):
        """Sets the upper CPU threshold."""
        self.__upper_cpu_threshold = upper

    @lazy_property
    def upper_ram_threshold(self):
        """A number between 1 and 100 representing the percentage of RAM for 
        the upper RAM threshold."""
        return self.__upper_ram_threshold

    @upper_ram_threshold.setter
    def upper_ram_threshold(self, upper):
        """Sets upper ram threshold."""
        self.__upper_ram_threshold = upper

    @classmethod
    def all(cls, **kwargs):
        """List all Tiers."""
        res = Resource(cls.PATH)
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

    @required_attrs(['name',
					 'description',
					 'budget',
					 'deployment',
					 'minimum_servers',
					 'maximum_servers',
					 'breach_period_in_minutes',
					 'cooldown_period_in_minutes',
					 'lower_cpu_threshold',
					 'upper_cpu_threshold',
					 'lower_ram_threshold',
					 'upper_ram_threshold' ])
    def create(self):
        """Creates a new tier

        :param callback: Optional callback to send the resulting :class:`Job`
        :raises: :class:`TierCreationException`
        """

        parms = [{'budget': self.budget,
                    'deployment': {'deploymentId': self.deployment},
                    'description': self.description,
                    'name': self.name,
                    'minimumServers': self.minimum_servers,
                    'maximumServers': self.maximum_servers,
                    'breachIncrement': self.breach_increment,
                    'breachPeriodInMinutes': self.breach_period_in_minutes,
                    'cooldownPeriodInMinutes': self.cooldown_period_in_minutes,
                    'lowerCpuThreshold': self.lower_cpu_threshold,
                    'upperCpuThreshold': self.upper_cpu_threshold,
                    'lowerRamThreshold': self.lower_ram_threshold,
                    'upperRamThreshold': self.upper_ram_threshold}]

        payload = {'addTier':camel_keys(parms)}

        response = self.post(data=json.dumps(payload))
        if self.last_error is None:
            self.load()
            return response
        else:
            raise TierCreationException(self.last_error)

class TierException(BaseException): 
    """Tier Exception"""
    pass

class TierCreationException(TierException):
    """Tier Creation Exception"""
    pass

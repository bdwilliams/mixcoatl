"""
mixcoatl.network.firewall_rule
--------------------
"""
from mixcoatl.resource import Resource
from mixcoatl.decorators.lazy import lazy_property
from mixcoatl.decorators.validations import required_attrs
from mixcoatl.utils import camel_keys
from mixcoatl.utils import camelize

import json

# pylint: disable-msg=R0902,R0904
class FirewallRule(Resource):
    """A firewall rule is an ingress or egress permission that grants or denies
    the right for traffic from a specific network source to a specific network
    destination."""
    PATH = 'network/FirewallRule'
    COLLECTION_NAME = 'rules'
    PRIMARY_KEY = 'firewall_rule_id'

    def __init__(self, firewall_rule_id = None, **kwargs):
        if 'detail' in kwargs:
            self.request_details = kwargs['detail']

        Resource.__init__(self)
        self.__firewall_rule_id = firewall_rule_id
        self.__start_port = None
        self.__direction = None
        self.__protocol = None
        self.__network_address = None
        self.__firewall = None
        self.__end_port = None
        self.__rule_provider_id = None
        self.end_port = None
        self.start_port = None
        self.direction = None
        self.network_address = None
        self.protocol = None

    @property
    def firewall_rule_id(self):
        """`int` - The unique enStratus id for this rule"""
        return self.__firewall_rule_id

    @lazy_property
    def firewall(self):
        """`dict` - The firewall to which this rule belongs"""
        # pylint: disable-msg=E0202
        return self.__firewall

    @firewall.setter
    def firewall(self, fwid):
        """Set the firewall."""
        self.__firewall = {'firewall_id': fwid}

    @lazy_property
    def rule_provider_id(self):
        """`str` - Provider's firewall rule ID"""
        return self.__rule_provider_id

    @required_attrs(['firewall', 
                    'network_address', 
                    'protocol', 
                    'direction', 
                    'start_port', 
                    'end_port'])
    def create(self, **kwargs):
        """Create a new firewall rule

            .. warning::

                Does not currently support adding ICMP rules

        :param reason: Reason for the new rule
        :type reason: str.
        :returns: `bool`
        :raises: :class:`FirewallRuleException`
        """

        if 'reason' not in kwargs:
            reason = 'Added by mixcoatl'
        else:
            reason = kwargs['reason']

        payload = {'add_rule':[{
            'firewall_id': self.firewall['firewall_id'],
            'direction': self.direction,
            'start_port': self.start_port,
            'end_port': self.end_port,
            'protocol': self.protocol,
            'reason': reason,
            'cidr' : self.network_address}]}

        if self.firewall_rule_id is not None:
            raise FirewallRuleException('Cannot modify existing firewall rule')

        self.post(self.PATH, data=json.dumps(camel_keys(payload)))

        if self.last_error is None:
            return True
        else:
            if self.last_request.status_code == 418:
                return True
            else:
                raise FirewallRuleException(self.last_error)

    @required_attrs(['firewall_rule_id'])
    def remove(self, reason):
        """Remove a firewall rule

        :param reason: Reason for removing the rule
        :type reason: str.
        :returns: `bool`
        :raises: :class:`FirewallRuleException`
        """

        params = {'reason': reason}
        self.delete(self.PATH+'/'+str(self.firewall_rule_id), params=params)

        if self.last_error is None:
            return True
        else:
            raise FirewallRuleException(self.last_error)

    @classmethod
    def all(cls, firewall_id, **kwargs):
        """List all rules for `firewall_id`

        :param firewall_id: The id of the firewall to list rules for
        :type firewall_id: int.
        :param detail: Level of detail to return - `basic` or `extended`
        :type detail: str.
        :param keys_only: Return only :attr:`firewall_rule_id` in results
        :type keys_only: bool.
        :returns: `list` of :attr:`firewall_rule_id` or :class:`FirewallRule`
        :raises: :class:`FirewallRuleException`
        """

        params = {}
        res = Resource(cls.PATH)
        res.request_details = 'none'
        if 'detail' in kwargs:
            request_details = kwargs['detail']
        else:
            request_details = 'extended'

        if 'keys_only' in kwargs:
            keys_only = kwargs['keys_only']
        else:
            keys_only = False

        params['firewallId'] = firewall_id
        fwrs = res.get(params=params)
        if res.last_error is None:
            keys = [fwrs[camelize(cls.PRIMARY_KEY)] \
            for fwr in fwrs[cls.COLLECTION_NAME]]
            if keys_only is True:
                rules = keys
            else:
                rules = []
                for fwr in fwrs[cls.COLLECTION_NAME]:
                    key = fwr[camelize(cls.PRIMARY_KEY)]
                    rule = cls(key)
                    rule.request_details = request_details
                    rule.load()
                    rules.append(rule)
            return rules
        else:
            raise FirewallRuleException(res.last_error)

# pylint: disable-msg=R0913
def add_rule(firewall_id, network, proto, direction, start, end, reason):
    """Add a firewall rule to a firewall

    >>> f = add_rule(136663, 
                     '10.1.1.1/32', 
                     'TCP', 
                     'INGRESS', 
                     15000, 
                     15000, 
                     'inbound api')

    """
    firewall = FirewallRule()
    firewall.firewall = firewall_id
    firewall.network_address = network
    firewall.protocol = proto
    firewall.direction = direction
    firewall.start_port = start
    firewall.end_port = end
    return firewall.create(reason=reason)

def delete_rule(rule_id, reason='rule removed by mixcoatl'):
    """Remove a firewall rule

    :param rule_id: The id of the firewall rule to remove
    :type rule_id: int.
    :param reason: The reason for removing the rule
    :type reason: string
    :returns: `bool`
    :raises: :class:`FirewallRuleException`
    """
    firewall = FirewallRule(rule_id)
    return firewall.remove(reason)

class FirewallRuleException(BaseException):
    """Generic Exception for FirewallRules"""
    pass

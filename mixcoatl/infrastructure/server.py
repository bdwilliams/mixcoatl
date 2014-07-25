"""
mixcoatl.infrastructure.server
--------------------
"""
from mixcoatl.resource import Resource
from mixcoatl.admin.job import Job
from mixcoatl.utils import camel_keys
from mixcoatl.decorators.validations import required_attrs
from mixcoatl.decorators.lazy import lazy_property

import json, time

# pylint: disable-msg=R0902,R0904,R0912
class Server(Resource):
    """A server is a virtual machine running within a data center."""

    PATH = 'infrastructure/Server'
    COLLECTION_NAME = 'servers'
    PRIMARY_KEY = 'server_id'

    def __init__(self, server_id=None):
        Resource.__init__(self)
        self.__server_id = server_id
        self.__agent_version = None
        self.__customer = None
        self.__cm_account = None
        self.__cloud = None
        self.__owning_groups = None
        self.__owning_user = None
        self.__platform = None
        self.__personalities = None
        self.__private_ip_addresses = None
        self.__public_ip_address = None
        self.__region = None
        self.__provider_id = None
        self.__public_ip_addresses = None
        self.__product = None
        self.__start_date = None
        self.__stop_date = None
        self.__status = None
        self.__scripts = None
        self.__run_list = None
        self.__architecture = None
        self.__pause_after = None
        self.__machine_image = None
        self.__p_scripts = None
        self.__vlan = None
        self.__name = None
        self.__label = None
        self.__description = None
        self.__cm_scripts = None
        self.__data_center = None
        self.__environment = None
        self.__provider_product_id = None
        self.__firewalls = None
        self.__keypair = None
        self.__budget = None
        self.__terminate_after = None

    @property
    def server_id(self):
        """`int` - The enStratus ID of this server"""
        return self.__server_id

    @lazy_property
    def agent_version(self):
        """`int` - The version of the enStratus agent if installed."""
        return self.__agent_version

    @lazy_property
    def cloud(self):
        """`dict` - The cloud provided where the instance is located."""
        return self.__cloud

    @lazy_property
    def label(self):
        """`str` - The label assigned to the server"""
        return self.__label

    @label.setter
    def label(self, label):
        """Set the label"""
        self.__label = label

    @lazy_property
    def customer(self):
        """`dict` - The customer account for the server."""
        return self.__customer

    @lazy_property
    def data_center(self):
        """`dict` - The specific datacenter where the instance is located."""
        return self.__data_center

    @data_center.setter
    def data_center(self, data):
        """Set the data center."""
        self.__data_center = {u'data_center_id': data}

    @lazy_property
    def cm_account(self):
        """The configuration management account associated with the 
        environment, parameters, and runList you want to be applied to the 
        server post-launch."""
        return self.__cm_account

    @lazy_property
    def environment(self):
        """The configuration management account associated with the 
        environment, parameters, and runList you want to be applied to the 
        server post-launch."""
        return self.__environment

    @environment.setter
    def environment(self, environment):
        """Set the environment."""
        self.__environment = {u'sharedEnvironmentCode': environment}

    @cm_account.setter
    def cm_account_id(self, cai):
        """Set the CM account id."""
        self.__cm_account = {u'cmAccountId': cai}

    @lazy_property
    def cm_scripts(self):
        """Scripts during server launch."""
        return self.__cm_scripts

    @cm_scripts.setter
    def cm_scripts(self, css):
        """Set CM scripts."""
        script = css.split(",")
        scs = []
        for cms in script:
            scs.append({u'sharedScriptCode': cms})

        self.__cm_scripts = scs

    @lazy_property
    def p_scripts(self):
        """Scripts associated with launch."""
        return self.__p_scripts

    @p_scripts.setter
    def p_scripts(self, scripts):
        """Set the scripts"""
        script = scripts.split(",")
        pscm = []
        for cms in script:
            pscm.append({'sharedPersonalityCode': cms})

        self.__p_scripts = pscm

    @lazy_property
    def description(self):
        """The description of the server"""
        # pylint: disable-msg=E0202,R0801
        return self.__description

    @description.setter
    def description(self, desc):
        """Set the description."""
        # pylint: disable-msg=E0202,R0801
        self.__description = desc

    @lazy_property
    def machine_image(self):
        """`dict` - The machine image to use/used to provision the server"""
        return self.__machine_image

    @machine_image.setter
    def machine_image(self, mis):
        """Identifies the machine from which this server was built. Some clouds
        may allow this value to be empty."""
        self.__machine_image = {u'machine_image_id': mis}

    @lazy_property
    def vlan(self):
        """`list` - The vlan to assign/assigned to the server"""
        return self.__vlan

    @vlan.setter
    def vlan(self, vlan):
        """Set the VLAN."""
        self.__vlan = {u'vlan_id': vlan}

    @lazy_property
    def firewalls(self):
        """`list` - The firewalls to assign/assigned to the server"""
        return self.__firewalls

    @firewalls.setter
    def firewalls(self, firewall):
        """Set the firewall."""
        self.__firewalls = firewall

    @lazy_property
    def name(self):
        """`str` - The name assigned/to assign to the server"""
        return self.__name

    @name.setter
    def name(self, name):
        """Set the server name."""
        self.__name = name

    @lazy_property
    def owning_groups(self):
        """`list` - The DCM groups owning the server."""
        return self.__owning_groups

    @lazy_property
    def owning_user(self):
        """`dict` - The enStratus user owning the server."""
        return self.__owning_user

    @lazy_property
    def platform(self):
        """`str` - The platform of the server *(i.e. `UBUNTU`)*."""
        return self.__platform

    @lazy_property
    def personalities(self):
        """`dict` - The personalities associated with the server"""
        return self.__personalities

    @lazy_property
    def private_ip_addresses(self):
        """`list` - The private ip addresses assigned to the server."""
        return self.__private_ip_addresses

    @lazy_property
    def public_ip_address(self):
        """`str` - The public ip address of the server."""
        return self.__public_ip_address

    @lazy_property
    def public_ip_addresses(self):
        """`list` - The list of public ip addresses of the server."""
        return self.__public_ip_addresses

    @lazy_property
    def region(self):
        """`dict` - The region where the server is located"""
        return self.__region

    @lazy_property
    def provider_product_id(self):
        """`str` - The provider's product identifier for the server 
        *(i.e. `m1.large`)*"""
        return self.__provider_product_id

    @provider_product_id.setter
    def provider_product_id(self, ids):
        """Sets provider product id"""
        self.__provider_product_id = ids

    @lazy_property
    def provider_id(self):
        """`str` - The provider's identifier for the server 
        *(i.e. `i-abcdefg`)*"""
        return self.__provider_id

    @lazy_property
    def product(self):
        """`dict` - The enStratus product record for the server"""
        return self.__product

    @lazy_property
    def start_date(self):
        """`str` - The date the server was started"""
        return self.__start_date

    @lazy_property
    def stop_date(self):
        """`str` - The date the server was stopped"""
        return self.__stop_date

    @lazy_property
    def status(self):
        """`str` - The status of the server *(i.e. `RUNNING` or `PAUSED`)*."""
        return self.__status

    @lazy_property
    def budget(self):
        """`int` - The budget code applied to the server."""
        return self.__budget

    @budget.setter
    def budget(self, budget):
        """`int` - The budget code to apply to the server."""
        self.__budget = budget

    @lazy_property
    def scripts(self):
        """`list` - The list of configuration management scripts of 
        the server.(Chef?)"""
        return self.__scripts

    @lazy_property
    def run_list(self):
        """`list` - The list of configuration management scripts of 
        the server.(Puppet?)"""
        return self.__run_list

    @lazy_property
    def architecture(self):
        """`str` - The architecture type of the server."""
        return self.__architecture

    @lazy_property
    def terminate_after(self):
        """`str` - The time the server automatically shuts down."""
        return self.__terminate_after

    @terminate_after.setter
    def terminate_after(self, terms):
        """If present, this server will automatically terminate at the 
        specified timestamp."""
        self.__terminate_after = terms

    @lazy_property
    def pause_after(self):
        """`str` - The time the server automatically pauses."""
        return self.__pause_after

    @property
    def keypair(self):
        """`str` - The keypair to assign

            .. note::
                enStratus does not track keypairs used to launch servers.
                This attribute is used only in the `launch()` call.
        """
        return self.__keypair

    @keypair.setter
    def keypair(self, kps):
        """Set keypair."""
        self.__keypair = kps

    def reload(self):
        """Reload resource data from API calls"""
        if self.server_id is not None:
            self.load()
        elif self.current_job is None:
            self.load()
        else:
            if Job.wait_for(self.current_job):
                job = Job(self.current_job)
                self.__server_id = job.message
                self.load()
            else:
                return self.last_error

    @required_attrs(['server_id'])
    def destroy(self, reason='no reason provided'):
        """Terminate server instance with reason :attr:`reason`

        :param reason: The reason for terminating the server
        :type reason: str.
        :returns: bool -- Result of API call
        """
        path = self.PATH+"/"+str(self.server_id)
        qopts = {'reason':reason}
        return self.delete(path, params=qopts)

    @required_attrs(['server_id'])
    def pause(self, reason=None):
        """Pause the server instance with reason :attr:`reason`

        :param reason: The reason for pausing the server
        :type reason: str.
        :returns: Job -- Result of API call
        """
        path = '%s/%s' % (self.PATH, str(self.server_id))
        payload = {'pause':[{}]}

        if reason is not None:
            payload['pause'][0].update({'reason':reason})

        return self.put(path, data=json.dumps(payload))

    @required_attrs(['server_id'])
    def extend_terminate(self, extend):
        """Extend server terminateAfter."""
        path = '%s/%s' % (self.PATH, str(self.server_id))
        qopts = {'terminateAfter':extend}
        return self.delete(path, params=qopts)

    @required_attrs(['server_id'])
    def start(self, reason=None):
        """Start the paused server instance with reason :attr:`reason`

        :param reason: The reason for starting the server
        :type reason: str.
        :returns: Job -- Result of API call
        """
        path = '%s/%s' % (self.PATH, str(self.server_id))
        payload = {'start':[{}]}

        if reason is not None:
            payload['start'][0].update({'reason':reason})

        return self.put(path, data=json.dumps(payload))

    @required_attrs(['server_id'])
    def stop(self, reason=None):
        """Stop the server instance with reason :attr:`reason`

        :param reason: The reason for stopping the server
        :type reason: str.
        :returns: Job -- Result of API call
        """
        path = '%s/%s' % (self.PATH, str(self.server_id))
        payload = {'stop':[{}]}

        if reason is not None:
            payload['stop'][0].update({'reason':reason})

        return self.put(path, data=json.dumps(payload))

    @required_attrs(['provider_product_id', 'machine_image', 'description',
                    'name', 'data_center', 'budget'])
    def launch(self, callback=None):
        """Launches a server with the configured parameters

        >>> def cb(j): print(j)
        >>> s = Server()
        >>> s.provider_product_id = 'm1.large'
        >>> s.machine_image = 12345
        >>> s.description = 'my first launch'
        >>> s.name = 'server-1-test'
        >>> s.data_center = 54321
        >>> s.keypair = 'my-aws-keypair'
        >>> s.launch(callback=cb)

        :param callback: Optional callback to send the results of the API call
        :type callback: func.
        :returns: int -- The job id of the launch request
        :raises: :class:`ServerLaunchException`
            , :class:`mixcoatl.decorators.validations.ValidationException`
        """
        optional_attrs = ['vlan', 'firewalls', 'keypair', 'label', 
        'cm_account', 'environment', 'cm_scripts', 'p_scripts', 
        'volumeConfiguration']
        if self.server_id is not None:
            raise ServerLaunchException('Cannot launch an already \
                                        running server: %s' % self.server_id)

        payload = {'launch':
                    [{
                        'productId': self.provider_product_id,
                        'budget': self.budget,
                        'machineImage': camel_keys(self.machine_image),
                        'description': self.description,
                        'name': self.name,
                        'dataCenter': camel_keys(self.data_center)
                    }]}

        for oas in optional_attrs:
            try:
                if getattr(self, oas) is not None:
                    if oas == 'cm_scripts':
                        payload['launch'][0].update({'scripts':\
                                                    getattr(self, oas)})
                    elif oas == 'p_scripts':
                        payload['launch'][0].update({'personalities':\
                                                    getattr(self, oas)})
                    elif oas == 'volumeConfiguration':
                        payload['launch'][0]\
                        .update({'volumeConfiguration':{u'raidlevel':'RAID0',\
                         u'volumeCount':1, u'volumeSize':2,\
                         u'fileSystem':'ext3', u'mountPoint':'/mnt/data'}})
                    elif oas == 'vlan':
                        payload['launch'][0]\
                        .update({'vlan':camel_keys(getattr(self, oas))})
                    else:
                        payload['launch'][0].update({oas:getattr(self, oas)})
            except AttributeError:
                pass

        self.post(data=json.dumps(payload))
        if self.last_error is None:
            if callback is not None:
                callback(self.current_job)
            else:
                return self.current_job
        else:
            raise ServerLaunchException(self.last_error)

    def duplicate(self, server):
        """Check for duplicate."""
        pass

    def wait_for(self, status='RUNNING', callback = None):
        """Blocks execution until the current server has 
        status of :attr:`status`

        :param status: The status to expect before continuing 
            *(i.e. `RUNNING` or `PAUSED`)*
        :type status: str.
        :param callback: Optional callback to be called with the 
            final :class:`Server`` when ``status`` is reached
        :type callback: func.
        :raises: `ServerException`
        """
        if self.server_id is None:
            raise ServerException('Must be called with an existing server.')
        initial_status = self.status
        if self.last_error is None:
            if initial_status == status:
                return self
            while self.status != status:
                time.sleep(5)
                self.load()
                if self.last_error is not None:
                    raise ServerException(self.last_error)
                else:
                    continue
            if callback is not None:
                callback(self)
            else:
                return self

    @classmethod
    def all(cls, **kwargs):
        """Get a list of all known servers

        >>> Server.all()
        [{'server_id':1,...},{'server_id':2,...}]

        :returns: list -- a list of :class:`Server`
        :raises: ServerException
        """
        res = Resource(cls.PATH)
        res.request_details = 'basic'

        if 'params' in kwargs:
            params = kwargs['params']
        else:
            params = []
        get_data = res.get(params=params)
        if res.last_error is None:
            servers = [cls(server['serverId']) \
            for server in get_data[cls.COLLECTION_NAME]]
            return servers
        else:
            raise ServerException(res.last_error)

class ServerException(BaseException): 
    """Server Exception"""
    pass

class ServerLaunchException(ServerException): 
    """Server Launch Exception"""
    pass

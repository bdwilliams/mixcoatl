"""
mixcoatl.automation.launch_configuration
--------------------
"""
from mixcoatl.resource import Resource
from mixcoatl.decorators.lazy import lazy_property
from mixcoatl.decorators.validations import required_attrs
from mixcoatl.utils import camelize, camel_keys

import json

# pylint: disable-msg=R0902,R0904
class LaunchConfiguration(Resource):
    """A launch configuration is a set of launch characteristics for a tier in 
    a particular region. It defines region-specific things like the machine 
    image from which servers in the tier are launched."""
    PATH = 'automation/LaunchConfiguration'
    COLLECTION_NAME = 'launchConfigurations'
    PRIMARY_KEY = 'launch_configuration_id'

    def __init__(self, launch_configuration_id=None, **kwargs):
        Resource.__init__(self)
        self.__launch_configuration_id = launch_configuration_id
        self.__deployment = None
        self.__array_volume_capacity = None
        self.__array_volume_count = None
        self.__customer = None
        self.__cm_account = None
        self.__server_type = None
        self.__use_hypervisor_stats = None
        self.__snapshot_interval_in_minutes = None
        self.__use_encrypted_volumes = None
        self.__primary_product = None
        self.__firewalls = None
        self.__recovery_delay_in_minutes = None
        self.primary_product_id = None
        self.__secondary_product = None
        self.__secondary_machine_image = None
        self.__subnet = None
        self.__raid_level = None
        self.__tier = None
        self.__region = None
        self.__primary_machine_image = None
        self.__server_name_template = None
        self.__network = None

    @property
    def launch_configuration_id(self):
        """The unique DCM ID for this tier."""
        return self.__launch_configuration_id

    @property
    def deployment(self):
        """The deployment to which this launch configuration belongs."""
        return self.__deployment

    @property
    def array_volume_capacity(self):
        """The capacity in gigabytes of the volumes provisioned in the block 
        volume array supporting the services running in this tier. If the 
        volume count is less than 1 or the underlying cloud does not support 
        block volumes, any value here is meaningless. If your volume count is 
        greater than 1, this value must be at least 1 (or the minimum 
        allocation value for the underlying cloud provider)."""
        return self.__array_volume_capacity

    @property
    def array_volume_count(self):
        """The number of volumes in the block volume array supporting the 
        services running in this tier. This value can be zero if you want 
        services to run on the root volume or if the underlying cloud does not
        support block volumes."""
        return self.__array_volume_count

    @lazy_property
    def customer(self):
        """The customer to which this launch configuration belongs."""
        return self.__customer

    @lazy_property
    def cm_account(self):
        """The configuration management account to use when configuring 
        servers launched based on this launch configuration."""
        return self.__cm_account

    @lazy_property
    def firewalls(self):
        """The list of firewalls that will protect servers provisioned in this 
        launch configuration."""
        return self.__firewalls

    @firewalls.setter
    def firewalls(self, firewall):
        """Sets the firewalls."""
        self.__firewalls = firewall

    @lazy_property
    def network(self):
        """The network into which servers will be launched. If not specified, 
        the server will be launched into the default network for the cloud."""
        return self.__network

    @network.setter
    def network(self, net):
        """Sets the network."""
        self.__network = net

    @lazy_property
    def primary_machine_image(self):
        """The primary machine image."""
        return self.__primary_machine_image

    @primary_machine_image.setter
    def primary_machine_image(self, pmi):
        """Set the primary machine image."""
        self.__primary_machine_image = pmi

    @lazy_property
    def primary_product(self):
        """The primary product offering."""
        return self.__primary_product

    @primary_product.setter
    def primary_product(self, product):
        """Set the primary product offering."""
        self.__primary_product = product

    @lazy_property
    def raid_level(self):
        """Defines the RAID level to use if installing services across multiple
        block volumes. If using multiple block volumes, we recommend using 
        RAID0. Other RAID levels provide no value in the cloud."""
        return self.__raid_level

    @raid_level.setter
    def raid_level(self, raid):
        """Sets the raid level."""
        self.__raid_level = raid

    @lazy_property
    def recovery_delay_in_minutes(self):
        """The number of minutes Enstratius will wait after it loses 
        communication with a virtual machine before it will remove that virtual
        machine from the tier supported by this launch configuration. That 
        removal may cause DCM to execute an auto-recovery. Note that 
        DCM will handle over failures immediately regardless of this value."""
        return self.__recovery_delay_in_minutes

    @recovery_delay_in_minutes.setter
    def recovery_delay_in_minutes(self, delay):
        """Sets recovery delay."""
        self.__recovery_delay_in_minutes = delay

    @lazy_property
    def region(self):
        """The region for which this launch configuration is configured. You 
        may have at most one launch configuration per region for a tier."""
        return self.__region

    @region.setter
    def region(self, region):
        """Set region."""
        self.__region = region

    @lazy_property
    def secondary_machine_image(self):
        """The machine image to use for provisioning servers two and on in this
        launch configuration.  Secondary products and machine images can be 
        desirable for master versus slave servers in replicated 
        configurations."""
        return self.__secondary_machine_image

    @secondary_machine_image.setter
    def secondary_machine_image(self, smi):
        """Set the secondary machine image."""
        self.__secondary_machine_image = smi

    @lazy_property
    def secondary_product(self):
        """The server product to use for provisioning servers two and on in 
        this launch configuration.   Secondary products and machine images can
        be desirable for master versus slave servers in replicated 
        configurations."""
        return self.__secondary_product

    @secondary_product.setter
    def secondary_product(self, spm):
        """Set secondary product."""
        self.__secondary_product = spm

    @lazy_property
    def server_name_template(self):
        """The template Enstratius will use in naming servers provisioned 
        through this launch configuration. """
        return self.__server_name_template

    @server_name_template.setter
    def server_name_template(self, snt):
        """Set server template name."""
        self.__server_name_template = snt

    @lazy_property
    def server_type(self):
        """What type of servers are launched in this launch configuration."""
        return self.__server_type

    @server_type.setter
    def server_type(self, sts):
        """Set server type."""
        self.__server_type = sts

    @lazy_property
    def snapshot_interval_in_minutes(self):
        """If the services running on servers under this launch configuration 
        run on independent block storage devices, Enstratius will automatically
        snapshot those volumes according to the interval specified here. If the
        interval is daily, the snapshots will occur during the deployment’s 
        backup window."""
        return self.__snapshot_interval_in_minutes

    @snapshot_interval_in_minutes.setter
    def snapshot_interval_in_minutes(self, siim):
        """Set snapshot interval in minutes."""
        self.__snapshot_interval_in_minutes = siim

    @lazy_property
    def subnet(self):
        """The subnet into which servers will be launched. """
        return self.__subnet

    @subnet.setter
    def subnet(self, subnet):
        """Set the subnet."""
        self.__subnet = subnet

    @property
    def tier(self):
        """The tier whose services run on the servers provisioned through this
        launch configuration."""
        return self.__tier

    @tier.setter
    def tier(self, tier):
        """Set the tier."""
        self.__tier = tier

    @lazy_property
    def use_encrypted_volumes(self):
        """If you are allocating volumes to your services in this launch 
        configuration, this value indicates whether those volumes should be 
        encrypted or not."""
        return self.__use_encrypted_volumes

    @use_encrypted_volumes.setter
    def use_encrypted_volumes(self, uev):
        """Set whether to use encrypted volumes."""
        self.__use_encrypted_volumes = uev

    @lazy_property
    def use_hypervisor_stats(self):
        """Determines whether the performance metrics used in auto-scaling 
        should be pulled from any hypervisor statistics provided by the 
        cloud."""
        return self.__use_hypervisor_stats

    @use_hypervisor_stats.setter
    def use_hypervisor_stats(self, uhs):
        """Set whether to use hypervisor stats."""
        self.__use_hypervisor_stats = uhs

    @classmethod
    def all(cls, **kwargs):
        """List all Launch Configurations"""
        res = Resource(cls.PATH)
        if 'details' in kwargs:
            res.request_details = kwargs['details']
        else:
            res.request_details = 'basic'

        lcs = res.get()
        if res.last_error is None:
            return [cls(i[camelize(cls.PRIMARY_KEY)]) \
            for i in lcs[cls.COLLECTION_NAME]]
        else:
            return res.last_error

    @required_attrs(['tier',
					 'region',
					 'primary_machine_image',
					 'primary_product_id'
					 ])

    def create(self):
        """Creates a new launch configuration

        :raises: :class:`TierCreationException`
        """
        #lc.name = name
        #lc.region = region
        #lc.primary_product = primary_product_id
        #lc.secondary_product = secondary_product_id
        #lc.primary_machine_image = primary_machine_image
        #lc.secondary_machine_image = secondary_machine_image
        #lc.server_name_template = server_name_template
        #lc.tier = tier
        #lc.firewall = firewall
        #lc.region = region

        parms = [{'tier':{'tierId':self.tier},
                 'primaryMachineImage':
                    {'machineImageId':self.primary_machine_image},
                 'primaryProduct':{'productId':self.primary_product_id},
                 'firewalls':[{'firewallId':self.firewalls}],
                 'region':{'regionId':self.region}}]

        payload = {'addLaunchConfiguration':camel_keys(parms)}

        response = self.post(data=json.dumps(payload))
        if self.last_error is None:
            self.load()
            print response
            return response
        else:
            raise LaunchConfigurationCreationException(self.last_error)

class LaunchConfigurationException(BaseException): 
    """Launch Configuration Exception"""
    pass

class LaunchConfigurationCreationException(LaunchConfigurationException):
    """Launch Configuration Creation Exception"""
    pass

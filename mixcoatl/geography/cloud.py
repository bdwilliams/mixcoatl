"""
mixcoatl.geograpy.cloud
--------------------
"""
from mixcoatl.resource import Resource
from mixcoatl.decorators.lazy import lazy_property

# pylint: disable-msg=R0902,R0904
class Cloud(Resource):
    """A cloud is a distinct infrastructure providing cloud services. It may be
    a private cloud or a public cloud and may provide infrastructure or 
    platform services. """
    PATH = 'geography/Cloud'
    COLLECTION_NAME = 'clouds'
    PRIMARY_KEY = 'cloud_id'

    def __init__(self, cloud_id = None, **kwargs):
        Resource.__init__(self)
        self.__cloud_id = cloud_id
        self.__cloud_provider_console_url = None
        self.__cloud_provider_logo_url = None
        self.__cloud_provider_name = None
        self.__name = None
        self.__status = None
        self.__private_cloud = None
        self.__compute_delegate = None
        self.__compute_endpoint = None
        self.__compute_account_number_label = None
        self.__compute_access_key_label = None
        self.__compute_x509_cert_label = None
        self.__compute_x509_key_label = None
        self.__compute_secret_key_label = None
        self.__documentation_label = None

    @property
    def cloud_id(self):
        """`int` - The unique enStratus id for this cloud"""
        return self.__cloud_id

    @lazy_property
    def cloud_provider_console_url(self):
        """`str` - URL of the cloud provider's own console"""
        return self.__cloud_provider_console_url

    @lazy_property
    def cloud_provider_logo_url(self):
        """`str` - enStratus installation URL to this cloud's logo"""
        return self.__cloud_provider_logo_url

    @lazy_property
    def cloud_provider_name(self):
        """`str` - The name of the vendor providing the cloud"""
        return self.__cloud_provider_name

    @lazy_property
    def compute_account_number_label(self):
        """`str` - enStratus localized label key for the cloud's user account 
        number"""
        return self.__compute_account_number_label

    @lazy_property
    def compute_access_key_label(self):
        """`str` - enStratus localized label key for the cloud's API key"""
        return self.__compute_access_key_label

    @lazy_property
    def compute_x509_cert_label(self):
        """`str` - enStratus localized label key for the cloud's X509 
        certificate"""
        return self.__compute_x509_cert_label

    @lazy_property
    def compute_x509_key_label(self):
        """`str` - enStratus localized label key for the cloud's X509 key"""
        return self.__compute_x509_key_label

    @lazy_property
    def compute_delegate(self):
        """`str` - Dasein Cloud API Java class for interacting with this 
        cloud"""
        return self.__compute_delegate

    @lazy_property
    def compute_endpoint(self):
        """`str` - Comma-separated list of cloud API endpoints"""
        return self.__compute_endpoint

    @lazy_property
    def compute_secret_key_label(self):
        """`str` - enStratus localized label key for the cloud's API 
        secret key"""
        return self.__compute_secret_key_label

    @lazy_property
    def documentation_label(self):
        """`str` - enStratus localized label key"""
        return self.__documentation_label

    @lazy_property
    def name(self):
        """`str` - The enStratus name of the cloud"""
        return self.__name

    @lazy_property
    def private_cloud(self):
        """`bool` - If the cloud is a private cloud or not"""
        return self.__private_cloud

    @lazy_property
    def status(self):
        """`str` - Status of the cloud in enStratus"""
        return self.__status

    @classmethod
    def all(cls, keys_only=False, **kwargs):
        """Return all clouds

        :param keys_only: Return :attr:`cloud_id` instead of :class:`Cloud`
        :type keys_only: bool.
        :param detail: The level of detail to return - `basic` or `extended`
        :type detail: str.
        :returns: `list` of :class:`Cloud` or :attr:`cloud_id`
        """
        res = Resource(cls.PATH)
        res.request_details = 'basic'
        params = {}

        if 'public_only' in kwargs:
            params['publicOnly'] = kwargs['public_only']
        if 'status' in kwargs:
            params['status'] = kwargs['status']

        cld = res.get(params=params)

        if res.last_error is None:
            if keys_only is True:
                return [i['cloudId'] for i in cld[cls.COLLECTION_NAME]]
            else:
                clouds = []
                for i in cld[cls.COLLECTION_NAME]:
                    cloud = cls(i['cloudId'])
                    if 'detail' in kwargs:
                        cloud.request_details = kwargs['detail']
                    cloud.params = params
                    cloud.load()
                    clouds.append(cloud)
                return clouds
        else:
            return res.last_error

"""
mixcoatl.resource
------------------
"""
from mixcoatl.settings.load_settings import settings
import mixcoatl.auth as auth
import requests as r
from mixcoatl.decorators.lazy import lazy_property
from mixcoatl.utils import camel_keys

# pylint: disable-msg=R0902
class Resource(object):
    """The base class for all resources returned from an DCM API call
    By default all resources are largely represented as a `dict`-alike object
    that mirrors the JSON response from the DCM API with keys converted
    from camel-case to snake-case.

    For instance:

        * The DCM API JSON for a resource looks something like this:

            .. code-block:: yaml

                {
                  'someId':1,
                  'name':'my-name',
                  'cloud':{'cloudId':12345}
                }

        * All keys (nested or top-level) will be converted to snake-case:
            - `someId` becomes `some_id`
            - `cloudId` becomes `cloud_id`
        * The top-level keys will be converted to getters 
            (and in some cases - setters) on the Resource.
            - `some_id` will now be the resource's primary identifier: 
            `resource.some_id`
            - `name` will likely be a getter and a setter as `name` is 
            usually a mutable attributes
            - `cloud` will be converted to a setter with a value of 
            `{'cloud_id':123345}`
        * In cases where a setter would actually need to set a nested value, 
        it will do so. However the getter will still return the original data 
        structure as appropriate

        .. warning::

            The Resource object, while looking much like a `dict`, is not a 
            `dict` proper.
            If you need an actual `dict`, call `to_dict()` on your instance.
    """

    #: The base request path of the resource
    PATH = None
    #: The top-level grouping of a resource in the API response
    COLLECTION_NAME = None
    #: The unique identifier of an individual resource
    PRIMARY_KEY = None

    def __init__(self, base_path=None, request_details = 'extended', **kwargs):

        if base_path is None:
            try:
                self.__path = self.__class__.PATH
            except:
                raise AttributeError('you must override base_path')
        else:
            self.__path = base_path

        if 'request_details' in kwargs:
            self.__request_details = kwargs['request_details']
            del kwargs['request_details']
        else:
            self.__request_details = 'extended'

        if 'params' in kwargs:
            self.__params = kwargs['params']
        else:
            self.__params = {}
        self.__last_request = None
        self.__last_error = None
        self.__current_job = None
        self.__payload_format = 'json'
        self.__request_details = request_details
        self.pending_changes = {}
        self.loaded = False

    def __props(self):
        """List of properties and lazy properties for a given resource"""
        items = self.__class__.__dict__.items()
        prop = [k for k, v in items if type(v) in [lazy_property, property]]
        rp1 = ['last_error', 'path', 'last_request', \
                    'current_job', 'request_details']
        return prop + rp1


    def __repr__(self):
        from mixcoatl.utils import convert
        data = {}
        for val in self.__props():
            try:
                if val == 'last_request':
                    data[val] = str(getattr(self, val))
                else:
                    data[val] = getattr(self, val)
            except AttributeError:
                data[val] = None
            except KeyError:
                data[val] = None
        return repr(convert(data))

    @property
    def request_details(self):
        """The level of detail used in the API call: `basic` or `extended`"""
        return self.__request_details

    @request_details.setter
    def request_details(self, level):
        """Sets the level of detail used in the API call"""
        self.__request_details = level

    @property
    def payload_format(self):
        """The format of the payload: `json` or `xml`"""
        return self.__payload_format

    @payload_format.setter
    def payload_format(self, p_format):
        """Sets the format of the payload"""
        self.__payload_format = p_format

    @property
    def path(self):
        """The path used in the API request (e.g. ``admin/Job``)"""
        return self.__path

    @path.setter
    def path(self, path):
        """Sets the path used in the API request"""
        self.__path = path

    @property
    def last_request(self):
        """The :class:`Request` object of the most recent API call"""
        return self.__last_request

    @last_request.setter
    def last_request(self, last_request):
        """Sets the last request of the most recent API call"""
        self.__last_request = last_request

    @property
    def last_error(self):
        """The last error message, if any, from the most recent API call"""
        return self.__last_error

    @last_error.setter
    def last_error(self, last_error):
        """Sets the last error, if any, of the most recent API call"""        
        self.__last_error = last_error

    @property
    def current_job(self):
        """The current :class:`Job`, if any, of an asynchronous API call"""
        return self.__current_job

    @current_job.setter
    def current_job(self, current_job):
        """Sets the current job from the last API call"""
        self.__current_job = current_job

    @property
    def params(self):
        """The parameters that are passed to a specific function."""
        return self.__params

    @params.setter
    def params(self, params):
        """Sets the available paramaters"""
        self.__params = params

    def load(self):
        """(Re)load the current object's attributes from an API call"""
        from mixcoatl.utils import uncamel_keys
        reserved_words = ['type']
        path = self.PATH+"/"+str(getattr(self, self.__class__.PRIMARY_KEY))

        #self.request_details = 'extended'
        scopeit = self.get(path, params=camel_keys(self.params))
        if self.last_error is None:
            scope = uncamel_keys(scopeit[self.__class__.COLLECTION_NAME][0])
            for k in scope.keys():
                if k in reserved_words:
                    the_key = 'e_'+k
                else:
                    the_key = k
                new_key = '_%s__%s' % (self.__class__.__name__, the_key)
                if the_key not in self.__props():
                    raise AttributeError('Key found without accessor: %s' % k)
                else:
                    setattr(self, new_key, scope[k])
                    self.loaded = True
        else:
            return self.last_error

    # pylint: disable-msg=R0911,R0912,R0915
    def __doreq(self, method, **kwargs):
        """Performs the actual API call

        * calls `auth.get_sig` for signed headers
        * issues the requested :attr:`method` against the API endpoint
        * Handles requests appropriately based on sync/async nature of the call
            based on DCM API documentation
        """
        failures = [400, 403, 404, 409, 500, 501, 503]
        sig = auth.get_sig(method, self.path)
        url = settings.endpoint+'/'+self.path
        ssl_verify = settings.ssl_verify

        if self.payload_format == 'xml':
            payload_format = 'application/xml'
        elif self.payload_format == 'json':
            payload_format = 'application/json'
        else:
            raise AttributeError('Wrong format: %s' % self.payload_format)

        headers = {'x-esauth-access': sig['access_key'],
        'x-esauth-timestamp': str(sig['timestamp']),
        'x-esauth-signature': str(sig['signature']),
        'x-es-details': self.request_details,
        'Accept': payload_format,
        'User-Agent': sig['ua']}

        results = r.request(method, 
                            url, 
                            headers=headers, 
                            verify=ssl_verify, 
                            **kwargs)

        self.last_error = None
        self.last_request = results

        if self.payload_format == 'xml':
            return results

        if results.status_code in failures:
            try:
                err = results.json()
                self.last_error = err['error']['message']
            except ValueError:
                self.last_error = results.content
            return self.last_error

        if method == 'GET':
            try:
                results.raise_for_status()
                self.last_error = None
                return results.json()
            except r.exceptions.HTTPError:
                try:
                    err = results.json()
                    self.last_error = err['error']['message']
                except ValueError:
                    self.last_error = results.content
                return False
        if method == 'DELETE':
            if results.status_code == 202:
                self.current_job = results.json()['jobs'][0]['jobId']
                return results.json()
            elif results.status_code != 204:
                try:
                    err = results.json()
                    self.last_error = err['error']['message']
                except ValueError:
                    self.last_error = results.content
                return False
            else:
                return True
        if method == 'PUT':
            if results.status_code == 202:
                self.current_job = results.json()['jobs'][0]['jobId']
                return results.json()
            elif results.status_code == 204:
                return True
            else:
                try:
                    err = results.json()
                    self.last_error = err['error']['message']
                except ValueError:
                    self.last_error = results.content
                return False
        if method == 'POST':
            if results.status_code in [201, 202]:
                if results.status_code == 202:
                    self.current_job = results.json()['jobs'][0]['jobId']
                return results.json()
            else:
                try:
                    err = results.json()
                    self.last_error = err['error']['message']
                except ValueError:
                    self.last_error = results.content
                return False

    def set_path(self, path=None):
        """Sets API path"""
        if path is None:
            path = self.path
        else:
            self.path = path

    def get(self, path=None, **kwargs):
        """Perform an HTTP `GET` against the API for the resource"""
        self.set_path(path)
        return self.__doreq('GET', **kwargs)

    def post(self, path=None, **kwargs):
        """Perform an HTTP `POST` against the API for the resource"""
        self.set_path(path)
        return self.__doreq('POST', **kwargs)

    def put(self, path=None, **kwargs):
        """Perform an HTTP `PUT` against the API for the resource"""
        self.set_path(path)
        return self.__doreq('PUT', **kwargs)

    def delete(self, path=None, **kwargs):
        """Perform an HTTP `DELETE` against the API for the resource"""
        self.set_path(path)
        return self.__doreq('DELETE', **kwargs)

    def pprint(self):
        """The prettyprint formatted representation of the resource"""
        import pprint
        pprint.pprint(eval(repr(self)))

    def to_dict(self):
        """The `dict` representation of the current resource"""
        return eval(repr(self))

    def track_change(self, var, prev, new):
        """Tracks pending changes"""
        if prev == new:
            pass
        else:
            self.pending_changes[var] = {'old': prev, 'new':new}

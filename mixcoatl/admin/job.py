"""
mixcoatl.admin.job
------------------

Implements access to the DCM Job API
"""
from mixcoatl.resource import Resource
from mixcoatl.decorators.lazy import lazy_property
from mixcoatl.utils import camelize

import time

# pylint: disable-msg=R0902,R0904
class Job(Resource):
    """A job is an asynchronous process resulting from a client request that 
    resulted in a 202 ACCEPTED response. If the client cares about the ultimate 
    result of the original request, it can query for the job returned in the 
    initial response until the job completes."""
    PATH = 'admin/Job'
    COLLECTION_NAME = 'jobs'
    PRIMARY_KEY = 'job_id'

    def __init__(self, job_id = None, **kwargs):
        Resource.__init__(self)
        self.__job_id = job_id
        self.__status = None
        self.__description = None
        self.__message = None
        self.__start_date = None
        self.__end_date = None

    @property
    def job_id(self):
        """`int` The unique DCM id for this job"""
        return self.__job_id

    @lazy_property
    def status(self):
        """`str` The current status of this job"""
        return self.__status

    @lazy_property
    def description(self):
        """`str` The description of the running job."""
        return self.__description

    @lazy_property
    def message(self):
        """`str` A message describing the current operation disposition"""
        return self.__message

    @lazy_property
    def start_date(self):
        """`str` The date and time when the job was started"""
        return self.__start_date

    @lazy_property
    def end_date(self):
        """`str` The data and time when the job was completed
        `None` if :attr:`status is `RUNNING`
        """
        return self.__end_date

    @classmethod
    def all(cls, keys_only=False):
        """Get all jobs


        :param keys_only: Only return :attr:`job_id` instead of :class:`Job`
        :type keys_only: bool.
        :returns: `list` of :class:`Job` or :attr:`job_id`
        :raises: :class:`JobException`
        """
        res = Resource(cls.PATH)
        jobs = res.get()
        if res.last_error is None:
            if keys_only is True:
                return [i[camelize(cls.PRIMARY_KEY)] \
                for i in jobs[cls.COLLECTION_NAME]]
            else:
                return [cls(i[camelize(cls.PRIMARY_KEY)]) \
                for i in jobs[cls.COLLECTION_NAME]]
        else:
            raise JobException(res.last_error)

    @classmethod
    def wait_for(cls, job_id, status='COMPLETE', callback = None):
        """Blocks execution until :attr:`job_id` returns :attr:`status`

        :param job_id: The ID of the job to wait on
        :type job_id: int.
        :param status: The status to expect before continuing
        :type status: str.
        :param callback: Optional callback to be called with final :class:`Job`
            when :attr:`status` is reached
        :type callback: func.
        :returns: `bool` - Result of job exectution
        :raises: :class:`JobException`
        """
        job = Job(job_id)
        job.load()
        if job.last_error is not None:
            raise JobException(job.last_error)
        else:
            while job.status != status:
                time.sleep(5)
                job.load()
                if job.status == 'ERROR':
                    break
                else:
                    continue
        if callback is not None:
            callback(job)
        else:
            return True

class JobException(BaseException):
    """Job Exception"""
    pass

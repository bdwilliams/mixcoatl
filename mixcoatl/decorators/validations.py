"""
mixcoatl.decorators.validations
--------------------
"""
from functools import wraps

def required_attrs(attrs):
    """decorator for marking a list of attributes before calling a function

    :param attrs: List of attributes that must be set
    :type attrs: list.
    :raises: `ValidationException`
    """
    def wrapper(method):
        """Checks for missing required attributes."""
        @wraps(method)
        def validate(obj, *args, **kwargs):
            """Validates missing attributes."""
            for ras in attrs:
                try:
                    if getattr(obj, ras) is None:
                        raise ValidationException('Required attribute "%s" \
                                                  is missing' % ras)
                except AttributeError:
                    raise ValidationException('Required attribute "%s" \
                                              is missing' % ras)
            return method(obj, *args, **kwargs)
        return validate
    return wrapper

class ValidationException(Exception): 
    """Validation Exception"""
    pass
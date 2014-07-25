"""Common helper utilities for use with mixcoatl"""

def uncamel(val):
    """Return the snake case version of :attr:`str`

    >>> uncamel('deviceId')
    'device_id'
    >>> uncamel('dataCenterName')
    'data_center_name'
    """
    import re
    snk = lambda val: re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', 
                           val).lower().strip('_')
    return snk(val)

def uncamel_keys(dict1):
    """Return :attr:`d1` with all keys converted to snake case

    >>> d = {'myThings':[{'thingId':1,'someThings':{'firstThing':'a_thing'}}]}
    >>> uncamel_keys(d)
    {'my_things': [{'thing_id': 1, 'some_things': {'first_thing': 'a_thing'}}]}
    """
    dict2 = dict()
    if not isinstance(dict1, dict):
        return dict1
    for k, val in dict1.iteritems():
        new_key = uncamel(k)
        if isinstance(val, dict):
            dict2[new_key] = uncamel_keys(val)
        elif isinstance(val, list):
            dict2[new_key] = [uncamel_keys(item) for item in val]
        else:
            dict2[new_key] = val
    return dict2

def camelize(val):
    """Return the camel case version of a :attr:`str`

    >>> camelize('this_is_a_thing')
    'thisIsAThing'
    """
    string = ''.join([t.title() for t in val.split('_')])
    return string[0].lower()+string[1:]

def camel_keys(dict1):
    """Return :attr:`d1` with all keys converted to camel case

    >>> b = {'my_things': [{'thing_id': 1, 'some_things': 
                                            {'first_thing': 'a_thing'}}]}
    >>> camel_keys(b)
    {'myThings': [{'thingId': 1, 'someThings': {'firstThing': 'a_thing'}}]}
    """
    dict2 = dict()
    if not isinstance(dict1, dict):
        return dict1
    for k, val in dict1.iteritems():
        new_key = camelize(k)
        if isinstance(val, dict):
            dict2[new_key] = camel_keys(val)
        elif isinstance(val, list):
            dict2[new_key] = [camel_keys(item) for item in val]
        else:
            dict2[new_key] = val
    return dict2

def convert(val):
    """Return :attr:`input` converted from :class:`unicode` to :class:`str`

    >>> convert(u'bob')
    'bob'
    >>> convert([u'foo', u'bar'])
    ['foo', 'bar']
    >>> convert({u'foo':u'bar'})
    {'foo': 'bar'}
    """
    if isinstance(val, dict):
        return dict((convert(key), convert(value)) for key, value \
                    in val.iteritems())
    elif isinstance(val, list):
        return [convert(element) for element in val]
    elif isinstance(val, unicode):
        return val.encode('utf-8')
    else:
        return val

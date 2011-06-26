import re
from datetime import timedelta


def parsetimedelta(time_str):
    """Converts an input string into a timedelta object. Based on code from: http://stackoverflow.com/questions/4628122/how-to-construct-a-timedelta-object-from-a-simple-string"""
    regex = re.compile(r'(?P<posneg>[+\-])?((?P<hours>\d+?)hr)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')
    
    parts = regex.match(time_str)
    parts = dict((k, v) for k, v in parts.groupdict().items() if v != None)
    if not parts:
        raise ValueError('Time string passed to parsetimedelta does not match required format.')
    time_params = {}
    
    posneg = 1
    if 'posneg' in parts:
        if parts['posneg'] == '-':
            posneg = -1
        del parts['posneg']
    
    for (name, param) in parts.iteritems():
        if param:
            time_params[name] = posneg * int(param)
    
    return timedelta(**time_params)

import re

def objectFormatter(object):
    if not isinstance(object, dict):
        return object or {}

    data = {}

    for key, value in object.items():

        match = re.match(r'([^\[]+)\[([^\]]+)\]', key)

        if match:
            new_key, sub_key = match.groups()

            if new_key not in data:
                data[new_key] = {}

            data[new_key][sub_key] = value
        else:
            data[key] = value
    
    return data
from uuid import UUID

__all__ = ['getuuid', 'getfloat', 'getstr', 'getint']


def getuuid(data, *keys):
    value = None
    for key in keys:
        value = data.get(key, {})
        return UUID(value) if value else None


def getfloat(data, *keys):
    value = None
    for key in keys:
        value = data.get(key, {})
        return float(value) if value else None


def getstr(data, *keys):
    value = None
    for key in keys:
        value = data.get(key, {})
        return str(value) if value else None


def getint(data, *keys):
    value = None
    for key in keys:
        value = data.get(key, {})
        return int(value) if value else None


from json import loads
from collections import namedtuple

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())

def json2obj(data): return loads(data, object_hook=_json_object_hook)

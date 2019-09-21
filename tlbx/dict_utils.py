from collections import OrderedDict
from collections.abc import MutableMapping

try:
    import simplejson as json
    from simplejson import JSONEncoder
except ImportError:
    print("WARNING: Failed to import simplejson, falling back to built-in json")
    import json
    from json import JSONEncoder


def set_missing_key(d, k, v):
    if k not in d:
        d[k] = v


# https://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge
def dictmerge(x, y, path=None, overwrite=False):
    if path is None:
        path = []
    for key in y:
        if key in x:
            if isinstance(x[key], (dict, MutableMapping)) and isinstance(
                y[key], (dict, MutableMapping)
            ):
                dictmerge(x[key], y[key], path + [str(key)], overwrite=overwrite)
            elif x[key] == y[key]:
                pass  # same leaf value
            else:
                if not overwrite:
                    raise Exception("Conflict at %s" % ".".join(path + [str(key)]))
                x[key] = y[key]
        else:
            x[key] = y[key]
    return x


# https://stackoverflow.com/questions/16664874/how-can-i-add-an-element-at-the-top-of-an-ordereddict-in-python
class OrderedDictPlus(OrderedDict):
    def prepend(self, key, value):
        self.update({key: value})
        self.move_to_end(key, last=False)


def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default


class JSONMixin:
    # Probably needs a better home
    def to_dict(self):
        if isinstance(self, dict):
            result = self
        else:
            result = self.__dict__.copy()
        for k, v in result.items():
            if hasattr(v, "to_dict"):
                result[k] = v.to_dict()
        return result

    # This is used for _defaults in JSON encoding
    def to_json(self):
        return self.__dict__

    def to_jsons(self):
        return json.dumps(self.__dict__)

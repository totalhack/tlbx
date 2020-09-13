from collections.abc import MutableMapping, Callable
from functools import wraps
from importlib import import_module
import inspect
import sys


def igetattr(obj, attr, *args):
    """Case-insensitive getattr"""
    for a in dir(obj):
        if a.lower() == attr.lower():
            return getattr(obj, a)
    if args:
        return args[0]
    raise AttributeError("type object '%s' has no attribute '%s'" % (type(obj), attr))


def get_class_vars(cls):
    return {
        i for i in dir(cls) if (not isinstance(i, Callable)) and (not i.startswith("_"))
    }


def get_class_var_values(cls):
    return {
        getattr(cls, i)
        for i in dir(cls)
        if (not isinstance(i, Callable)) and (not i.startswith("_"))
    }


class ClassVarContainsMeta(type):
    def __contains__(cls, key):
        return key in get_class_vars(cls)


class ClassValueContainsMeta(type):
    def __contains__(cls, key):
        return key in get_class_var_values(cls)


def import_object(name):
    if "." not in name:
        frame = sys._getframe(1)
        module_name = frame.f_globals["__name__"]
        object_name = name
    else:
        module_name = ".".join(name.split(".")[:-1])
        object_name = name.split(".")[-1]
    return getattr(import_module(module_name), object_name)


# https://stackoverflow.com/questions/1389180/automatically-initialize-instance-variables
def initializer(func):
    names, varargs, keywords, defaults = inspect.getargspec(func)

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        for name, arg in list(zip(names[1:], args)) + list(kwargs.items()):
            setattr(self, name, arg)
        if defaults:
            for i in range(len(defaults)):
                index = -(i + 1)
                if not hasattr(self, names[index]):
                    setattr(self, names[index], defaults[index])
        func(self, *args, **kwargs)

    return wrapper


class MappingMixin(MutableMapping):
    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)


# TODO: needs a better home?
def get_caller(depth=0):
    # Add 1 to depth so its the caller of the caller to this function
    return sys._getframe(depth + 1).f_back.f_code.co_name

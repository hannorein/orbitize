import sys
import types
import os

__version__ = '1.2.0'

# set Python env variable to keep track of example data dir
DATADIR = os.path.join(sys.prefix, 'orbitize_example_data')

# define functions for pickling class methods
def _pickle_method(method):
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
    for cls in cls.mro():
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)


if sys.version_info[0] < 3:
    import copy_reg
    copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)

"""Decorators to do implicit conversion of arguments into libglove extensions
"""
import inspect
from pathlib import Path, PosixPath, PurePosixPath, PureWindowsPath

PATH_TYPES = (Path, PosixPath, PurePosixPath, PurePosixPath)

def with_paths(ignore=None):
    if isinstance(ignore, str):
        ignore_names = (ignore,)
    else:
        ignore_names = []
    def _decorator(lib_fn):
        def _paths_to_bytes(*args, **kwargs):
            l_args = list(args)
            for index, arg in enumerate(l_args):
                if isinstance(arg, PATH_TYPES):
                    arg_name = inspect.getfullargspec(lib_fn)[0][index]
                    if not arg.exists() and arg_name not in ignore_names:
                        try:
                            class_name = getattr(inspect.getmodule(lib_fn), lib_fn.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
                        except:
                            class_name = "<Err: Class Not Found>"
                        raise ValueError("Path argument '{}' with value '{}' to function '{}.{}' does not exist!".format(arg_name,arg, class_name, lib_fn.__name__))
                    arg = str(arg).encode('utf-8')
                l_args[index] = arg
            args = tuple(l_args)
            d_kwargs = dict(kwargs)
            for kwarg, val in d_kwargs.items():
                if isinstance(val, PATH_TYPES):
                    val = str(val).encode('utf-8')
                d_kwargs[kwarg] = val
            kwargs = dict(d_kwargs)
            return lib_fn(*args, **kwargs)
        return _paths_to_bytes
    return _decorator
from enum import Enum

class Verbosity(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

def with_verbosity(lib_fn):
    def _cast_verbosity_arg(*args, **kwargs):
        verbosity_arg = kwargs.get("verbose")
        if isinstance(verbosity_arg, int):
            verbosity_arg = Verbosity(verbosity_arg)
            kwargs["verbose"] = verbosity_arg
        return lib_fn(*args, **kwargs)
    return _cast_verbosity_arg
from typing import Union

def EnumUnion(enum_type):
    return Union[int, enum_type]

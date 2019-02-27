# distutils: sources = src/lib/glove/test.c
# distutils: include_dirs = src/lib/glove

cimport ctest

def myfunc(int arg):
    return ctest.myfunc(arg)

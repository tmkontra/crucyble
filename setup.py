from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize


extensions = [
        Extension("crucyble.vocab_count", ["src/lib/vocab_count.pyx"]),
        Extension("crucyble.cooccur", ["src/lib/cooccur.pyx"]),
        Extension("crucyble.shuffle", ["src/lib/shuffle.pyx"]),
        Extension("crucyble.glove", ["src/lib/glove.pyx"]),
    ]

setup(
    ext_modules=cythonize(extensions)
)
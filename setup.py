from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_pkg_prefix = "src.crucyble.lib."

ext_sources = ("vocab_count", "cooccur", "shuffle", "glove")
ext_source_path = "src/lib/"
ext_source_ext = ".pyx"

extensions = [
    Extension(ext_pkg_prefix + e, [ext_source_path + e + ext_source_ext])
    for e in ext_sources
]

setup(
    ext_modules=cythonize(extensions)
)
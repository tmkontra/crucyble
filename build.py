from distutils.extension import Extension
from Cython.Build import cythonize
import toml

ext_pkg_prefix = "src.crucyble.lib."

ext_sources = ("vocab_count", "cooccur", "shuffle", "glove")
ext_source_path = "src/lib/"
ext_source_ext = ".pyx"

extensions = [
    Extension(ext_pkg_prefix + e, [ext_source_path + e + ext_source_ext])
    for e in ext_sources
]

extensions = cyth       onize(extensions)

def readme():
    with open("README.md", "r") as f:
        return f.read()

def pyproject_toml():
    with open("pyproject.toml", "r") as f:
        return toml.load(f)

def build(setup_kwargs):
    """Needed for the poetry building interface."""

    setup_kwargs.update({
        'ext_modules' : extensions,
        'include_dirs' : ["src/lib"],
        'description': pyproject_toml()['tool']['poetry']['description'],
        'long_description': readme(),
        "long_description_content_type": "text/markdown"
    })
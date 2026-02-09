from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

extensions = \
[
    Extension("filters_src", ["filters_src.pyx"])
]
setup(name = "filters_src", ext_modules = cythonize(extensions))

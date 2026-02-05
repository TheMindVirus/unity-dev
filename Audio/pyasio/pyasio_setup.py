from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

modules = \
[
    "pyasio.pyx",
]

libraries = \
[
    "ole32",
    "advapi32",
    "user32",
]

extensions = \
[
    Extension("pyasio", modules,
              language = "c++", libraries = libraries)
]
setup(name = "pyasio", ext_modules = cythonize(extensions))

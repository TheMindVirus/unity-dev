from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "blaskernel_cython",
        ["blaskernel_cython.pyx", "blaskernel_cpp.cpp"],
        language="c++",
    )
]
setup(name="blaskernel_cython", ext_modules=cythonize(extensions))

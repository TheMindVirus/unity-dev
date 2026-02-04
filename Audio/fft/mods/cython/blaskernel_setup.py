from Cython.Build import Cythonize
Cythonize.main(["-i", "blaskernel_src.pyx"])
#Cythonize.main(["-i", "blaskernel_cython.pyx", "blaskernel_cpp.cpp"])
import os
python_dir = "C:\\Python36\\python.exe"
os.system("cmd /k \"" + python_dir + " blaskernel_cython_setup.py build_ext --inplace && pause\"")

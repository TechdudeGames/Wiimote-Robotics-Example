#!/usr/bin/python3
from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = "libPWM",
    ext_modules = cythonize('libpwm.py'),  # accepts a glob pattern
)

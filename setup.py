from setuptools import setup, Extension, find_packages
import os
sources = ['microps/_core.c']
for f in os.listdir('microps/microops'):
    if f.endswith('.c'): sources.append(os.path.join('microps/microops', f))
setup(
    name='microps',
    version='1.3',
    packages=find_packages(),
    ext_modules=[Extension('microps._core', sources=sources, include_dirs=['microps/include'])],
)

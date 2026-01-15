# FILE: setup.py
from setuptools import setup, Extension
import os

# Get all .c files from microops directory
microops_dir = os.path.join('microps', 'microops')
microops_sources = []

if os.path.exists(microops_dir):
    microops_sources = [
        os.path.join(microops_dir, f) 
        for f in os.listdir(microops_dir) 
        if f.endswith('.c')
    ]
    print(f"Found {len(microops_sources)} micro operation files")
    for src in sorted(microops_sources):
        print(f"  - {src}")
else:
    print(f"WARNING: {microops_dir} not found!")

# Main extension module
core_extension = Extension(
    'microps._core',
    sources=['microps/_core.c'] + microops_sources,
    include_dirs=['microps/include'],
    extra_compile_args=['-O3', '-Wall'],
)

setup(
    name='microps',
    version='1.0.0',
    description='Micro Operations - Language semantics in Python via C extensions',
    author='holyarahippo06',
    packages=['microps', 'microps.wrappers'],
    ext_modules=[core_extension],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: C',
        'Topic :: Software Development :: Libraries',
    ],
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
)

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
    extra_compile_args=['-O3', '-Wall'] if os.name != 'nt' else ['/O2'],
)

# Read README with UTF-8 encoding (fixes Windows build issue)
long_description = ''
readme_path = 'README.md'
if os.path.exists(readme_path):
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            long_description = f.read()
    except Exception as e:
        print(f"Warning: Could not read README.md: {e}")
        long_description = 'Micro Operations - Language semantics in Python via C extensions'

setup(
    name='microps',
    version='1.3.0',
    description='Micro Operations - Language semantics in Python via C extensions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='holyarahippo06',
    author_email='',  # Add your email if desired
    url='https://github.com/holyarahippo06/microps',
    packages=['microps', 'microps.wrappers'],
    ext_modules=[core_extension],
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Compilers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: C',
        'Operating System :: OS Independent',
    ],
    keywords='language-semantics c-extension polyglot javascript lua ruby php',
    project_urls={
        'Bug Reports': 'https://github.com/holyarahippo06/microps/issues',
        'Source': 'https://github.com/holyarahippo06/microps',
    },
)

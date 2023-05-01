"""
Simple setup.py file such that this package using pip
# run: pip install .
# check: pip list
"""

from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.1',
    packages=find_packages(exclude=['src*']),
    license='Apache License 2.0',
    description='EDSA example python package',
    long_description=open('README.md', encoding='UTF-8').read(),
    long_description_content_type="text/markdown",
    # install_requires=['numpy', 'pandas'],
    url='',
    author='Rory Scott',
)

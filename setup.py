#!/usr/bin/env python
from os import path

import setuptools

from garpunapiclient import info


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

DEPENDENCIES = parse_requirements('requirements.txt')

setuptools.setup(
    name=info.__package_name__,
    version=info.__version__,

    description='Garpun API Client',
    long_description=long_description,

    url='https://github.com/garpun/garpun-api-python-client',

    author='Garpun Cloud',
    author_email='support@garpun.com',

    license="Apache 2.0",

    classifiers=[
        'Programming Language :: Python :: 3'
    ],
    install_requires=DEPENDENCIES,
    python_requires=">=3.4",
    packages=['garpunapiclient'],
    package_data={'': ['LICENSE']},
    include_package_data=True,
)

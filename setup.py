#!/usr/bin/env python

import os
import sys


from setuptools import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
doclink = """
Documentation
-------------

The full documentation is located at http://desdeo.it.jyu.fi"""

history = open('HISTORY.md').read()

long_desc = readme + '\n\n' + doclink + '\n\n' + history


setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

requirements = ['numpy', 'prompt-toolkit', 'scikit-learn', 'scipy']

setup(
    name='desdeo',
    url='desdeo.it.jyu.fi',
    license='MPL 2.0',
    author='Vesa Ojalehto',
    author_email='vesa.ojalehto@gmail.com',
    description='Open source library for for interactive multiobjective optimization',
    long_description=long_desc,
    version='0.1.0',

    packages=find_packages(include=['desdeo']),
    package_dir={'desdeo': 'desdeo'},
    install_requires=requirements,


    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)"
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)

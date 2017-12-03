#!/usr/bin/env python

from distutils.core import setup

try:
    with open('README.md') as f:
        long_description = f.read()
except IOError:
    long_description = ""

setup(name='grafana_api_client',
    version='0.2.0',
    url='https://github.com/htch/grafana_api_client',
    description='Grafana API wrapper/Basic Grafana API client library.',
    long_description=long_description,
    author_email='htch.git@gmail.com',
    keywords=['grafana'],
    platform='any',
    license='BSD',
    packages=["grafana_api_client"],
    requires=[
        "requests",
        "six"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development',
        'Topic :: System',
        'Topic :: Utilities',
    ]
)
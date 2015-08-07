#!/usr/bin/env python

from distutils.core import setup

setup(name='grafana_api_client',
    version='0.1.3',
    url='https://github.com/htch/grafana_api_client',
    description='Grafana API wrapper/Very basic Grafana API client library.',
    author='Pavel',
    author_email='htch.git@gmail.com',
    packages=["grafana_api_client"],
    requires=[
        "requests",
        "wsgiref",
    ]
)
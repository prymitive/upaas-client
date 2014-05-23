#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013-2014 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from __future__ import unicode_literals

from setuptools import setup, find_packages

try:
    from pip.req import parse_requirements
    required = {'install_requires': [str(r.req) for r in parse_requirements(
        'requirements.txt')]}
except ImportError:
    required = {}


setup(
    name='upaas-client',
    version='0.3.1',
    license='GPLv3',
    description='uPaaS CLI client',
    author='Łukasz Mierzwa',
    author_email='l.mierzwa@gmail.com',
    url='https://github.com/prymitive/upaas-client',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python',
    ],
    platforms=['Linux'],
    scripts=['upaas'],
    **required
)

#!/usr/bin/env python

from setuptools import setup

setup(
    name='prettylog',
    version='1.0',
    author='Rachel Bell',
    author_email='rachel.twu@gmail.com',
    description='Simple text logger and log-parser',
    install_requires=['Django>=1.3'],
    url='https://github.com/racheltwu/prettylog',
    packages=['prettylog'],
    license='BSD',
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
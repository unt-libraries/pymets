#!/usr/bin/env python

from setuptools import setup

setup(
    name='pymets',
    version='1.0.0',
    description='Python module for reading and writing METS files.',
    author='University of North Texas Libraries',
    author_email='mark.phillips@unt.edu',
    url='https://github.com/unt-libraries/pymets',
    license='BSD',
    packages=['pymets'],
    install_requires=[
        'lxml>=3.4.4',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)

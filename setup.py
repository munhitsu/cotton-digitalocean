#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='cotton-digitalocean',
    version='0.1.0',
    url='http://github.com/munhitsu/cotton-digitalocean',
    license='MIT',
    author='Mateusz Lapsa-Malawski',
    author_email='m@cr3.io',
    description='',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    platforms='any',
    install_requires=[
        'python-digitalocean',
        'cotton',
        'fabric'
    ],
    classifiers=[
    ],
)

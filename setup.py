#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='tplinkutil',
    version='1.0',
    description='A cli util to control TP-Link smart bulbs with cool features',
    author='Maciej Bratek',
    author_email='maclav3@gmail.com',
    url='https://github.com/maclav3/tplinkutil',
    packages=['tplinkutil'],
    requires=[
        'pyHS100',
        'colorlog',
        'GeoIP'
    ],
    entry_points={
        'console_scripts': [
            'tplinkutil = modes.__main__:main'
        ]
    }
)

#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='tplink-util',
    version='1.0',
    description='A cli util to control TP-Link smart bulbs with cool features',
    author='Maciej Bratek',
    author_email='maclav3@gmail.com',
    url='https://github.com/maclav3/tplink-util',
    packages=['tplink-util'],
    requires=['pyHS100', 'colorlog'],
    entry_points={
        'console_scripts': [
            'tplink-util = modes.__main__:main'
        ]
    }
)

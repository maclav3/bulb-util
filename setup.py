#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='bulbutil',
    version='1.0',
    description='A cli util to control smart bulbs with cool features. The TP-Link smart bubl interface is implemented'
                'for the time being. It may be easily extended with other bulb interfaces.',
    author='Maciej Bratek',
    author_email='maclav3@gmail.com',
    url='https://github.com/maclav3/bulbutil',
    packages=['bulbutil'],
    requires=[
        'pyHS100',
        'colorlog',
        'GeoIP', 'tzlocal', 'pytz', 'pysolar', 'numpy', 'arrow', 'configargparse'
    ],
    entry_points={
        'console_scripts': [
            'bulbutil = modes.__main__:main'
        ]
    }
)

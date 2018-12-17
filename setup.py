# -*- coding: UTF-8 -*-
"""
    setup
    ~~~~~

    :copyright: (c) 2018 by Oleksii Lytvyn.
    :license: MIT, see LICENSE for more details.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import grailkit


setup(
    name='grailkit',
    version=grailkit.__version__,
    author='Oleksii Lytvyn',
    author_email='programer95@gmail.com',
    description='Grail development kit',
    long_description=open('README.md').read(),
    url='https://bitbucket.org/alexlitvin/grailkit',
    download_url='https://bitbucket.org/alexlitvin/grailkit/get/default.zip',
    platforms='any',
    packages=['grailkit'],
    keywords=['framework', 'grail', 'development', 'osc', 'midi', 'dmx', 'utilities'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Telecommunications Industry',
        'Operating System :: OS Independent',
        'Environment :: Other Environment',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: System :: Networking',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License'
    ],
    install_requires=['pyserial', 'python-rtmidi']
)

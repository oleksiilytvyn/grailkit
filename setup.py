# -*- coding: UTF-8 -*-
"""
    setup
    ~~~~~

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
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
    long_description=open('README.rst').read(),
    url='https://bitbucket.org/grailapp/grail-kit',
    download_url='https://bitbucket.org/grailapp/grail-kit/get/default.zip',
    platforms='any',
    packages=['grailkit'],
    keywords=['framework', 'grail', 'development', 'osc', 'midi', 'artnet', 'dmx'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Networking',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    install_requires=['pyserial', 'python-rtmidi']
)

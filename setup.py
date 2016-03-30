#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Grail SDK
# Copyright (C) 2014-2016 Oleksii Lytvyn
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import grailkit


setup(
    name='grailkit',
    version=grailkit.__version__,
    author='Oleksii Lytvyn',
    author_email='grailapplication@gmail.com',
    description=(
        'Grail development kit'),
    long_description=open('README.rst').read(),
    url='https://bitbucket.org/grailapp/grail-kit',
    platforms='any',
    packages=['grailkit'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: System :: Networking',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=['PyQt5', ]
)

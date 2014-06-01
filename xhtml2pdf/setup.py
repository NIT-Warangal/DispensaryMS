#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

# Copyright 2010 Dirk Holtwick, holtwick.it
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools

    use_setuptools()

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name="xhtml2pdf",
    version="0.0.6",
    description="PDF generator using HTML and CSS",
    license="Apache License 2.0",
    author="Dirk Holtwick",
    maintainer="Daryl Yu",
    maintainer_email="hello+pleaseleavemealone@darylyu.com",
    url="http://www.xhtml2pdf.com",
    keywords="PDF, HTML, XHTML, XML, CSS",
    install_requires = ["html5lib", "pyPdf2", "Pillow", "reportlab>=2.2"],
    include_package_data=True,
    packages=find_packages(exclude=["tests", "tests.*"]),
    #    test_suite = "tests", They're not even working yet
    entry_points={
        'console_scripts': [
            'pisa = xhtml2pdf.pisa:command',
            'xhtml2pdf = xhtml2pdf.pisa:command',
        ]
    },
    long_description=README,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Documentation',
        'Topic :: Multimedia',
        'Topic :: Office/Business',
        'Topic :: Printing',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Fonts',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML',
        'Topic :: Utilities',
    ]
)

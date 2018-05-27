
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import re


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.match("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('currency_open_exchange')


LONG_DESCRIPTION = open('README.rst').read()

setup(
    name='currency_open_exchange',
    version=version,
    description='Currency conversion',
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        "Framework :: Django :: 1.10",
    ],
    keywords='currency-open-exchange',
    author='Anton Maistrenko',
    author_email='it2015maistrenko@gmail.com',
    url='',
    license="BSD",
    packages=find_packages(),
    include_package_data=True,
    test_suite='runtests',
    install_requires=[],
    zip_safe=False,
)
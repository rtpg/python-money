#!/usr/bin/env python
import os
from setuptools import setup, find_packages

from money.version import get_git_version

# For help with setuptools, see:
# http://packages.python.org/distribute/setuptools.html

loc = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(loc, 'README.md')) as f:
    README = f.read()

keywords = 'money currency finance'.split()

tests_require = [
    'django<1.4',
    'nose',
    'django_nose',
]

install_requires = []

extras_require = {
    'django':  ['Django<1.4',],
}

setup(
    name='python-money',
    version=get_git_version(),
    #packages=find_packages(exclude=['tests',]),
    packages=find_packages(),
    url='http://github.com/poswald/python-money',
    description='Primitives for working with money and currencies in Python',
    maintainer='Paul Oswald',
    maintainer_email='pauloswald@gmail.com',
    license='BSD',
    platforms=["any"],
    keywords=keywords,
    long_description=README,
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    #test_suite='nose.collector',
    test_suite='money.runtests.runtests',

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Office/Business :: Financial',
    ],)

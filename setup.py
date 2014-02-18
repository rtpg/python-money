#!/usr/bin/env python
import os, sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

from money.version import get_git_version

loc = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(loc, 'README.md')) as f:
    README = f.read()

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


keywords = 'money currency finance'.split()

tests_require = [
    'django',
    'pytest',
    'pytest-django',
]

install_requires = []

extras_require = {
    'django':  ['Django>1.4',],
}

setup(
    name='python-money',
    version=get_git_version(),
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
    cmdclass = {'test': PyTest},


    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Office/Business :: Financial',
    ],)

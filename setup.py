import os
from setuptools import setup
from distutils.util import convert_path
from distutils.command.install import INSTALL_SCHEMES
from version import get_git_version

# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# The following technique was lifted from Django's setup.py -po
# http://code.djangoproject.com/browser/django/trunk/setup.py
def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
start_dir = ''

for dirpath, dirnames, filenames in os.walk(start_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
        if dirname.startswith('docs'): del dirnames[i]
        
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

keywords = 'money currency finance'.split()

tests_require = [
    'django<1.5',
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
    packages=packages,
    data_files=data_files,
    url='http://github.com/poswald/python-money',
    description='Primitives for working with money and currencies in Python',
    maintainer='Paul Oswald',
    maintainer_email='pauloswald@gmail.com',
    long_description=open('README.md').read(),
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Office/Business :: Financial',
    ],
)

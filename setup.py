import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if os.path.exists('README.rst'):
    long_description = read('README.rst')
else:
    long_description = read('README.md')

install_requires = [
    'aiohttp',
    'pyasn1',
]

tests_require = [
    'pytest',
    'coverage',
    'pytest-cov',
    'pytest-mock',
]

def read_version():
    for line in open(os.path.join('kkdcp', '__init__.py'), 'r'):
        if line.startswith('__version__'):
            return line.split('=')[-1].strip().strip("'")


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name='py3-kkdcp',
    version=read_version(),
    author='Kai Blin',
    author_email='kai@samba.org',
    description='aio-based Python 3 implementation of MS-KKDCP',
    long_description=long_description,
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    packages=['kkdcp'],
    url='https://github.com/kblin/py3-kkdcp/',
    license='GNU General Public License v3 or later (GPLv3+)',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Networking',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
    extras_require={
        'testing': tests_require,
    },
)

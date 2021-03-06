from setuptools import setup
from setuptools.command.test import test as TestCommand
import io
import os
import sys

import domo

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.txt', 'CHANGES.txt')


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
    name='domo',
    version=domo.__version__,
    url='',
    license='',
    author=domo.__author__,
    tests_require=['pytest'],
    install_requires=[
    ],
    cmdclass={'test': PyTest},
    author_email=domo.__email__,
    description=domo.__doc__,
    long_description=long_description,
    packages=['domo'],
    include_package_data=True,
    platforms='any',
    test_suite='',
    classifiers=[
    ],
    extras_require={
        'testing': ['pytest'],
    }
)

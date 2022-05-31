import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='Delator',
    version='0.1',
    description='A simple tool that collects TODOS and reports them as GitHub issues.',
    long_description=read('README.md'),
    keywords='snitch, delator, todo finder',
    url='https://github.com/leirons/Delator',
    author='Ivan Grechka',
    author_email='grecigor11@gmail.com',
    include_package_data=True,
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',

        'Topic :: Internet :: WWW/HTTP'
    ],
)
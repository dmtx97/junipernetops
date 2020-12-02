from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'netopsauto',
    version = '0.1',
    packages=find_packages('./netopsauto'),
    description='Useful tools to automate your network',
    long_description=long_description,
    long_description_content_type = 'text/markdown',
    install_requires=['junos-eznc==2.5.4', 'netaddr==0.8.0', 'lxml==4.6.2', 'bcrypt==3.2.0', 'cryptography', 'textfsm', 'yamlordereddictloader==0.4.0', 'ncclient==0.6.9', 'scp==0.13.3', 'pyserial==3.5', 'transitions==0.8.5'],     
    url='https://github.com/dmtx97/netopsauto',
    author='Daniel Mendez',
    author_email='dmtx97@gmail.com'
)
from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'junipernetops',
    version = '0.1',
    packages=find_packages(),
    description='Useful tools to automate your Juniper network',
    long_description=long_description,
    long_description_content_type = 'text/markdown',
    install_requires=['junos-eznc', 'bcrypt', 'cryptography', 'textfsm'],     
    url='https://github.com/dmtx97/junipernetops',
    author='Daniel Mendez',
    author_email='dmtx97@gmail.com'
)
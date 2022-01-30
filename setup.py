
# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Derby Runner',
    version='0.1.0',
    description='Package for Managing Scouting Competitions',
    long_description=readme,
    author='farkle314159',
    author_email='farkle314159@gmail.com',
    url='https://github.com/farkle314159/derby_runner',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
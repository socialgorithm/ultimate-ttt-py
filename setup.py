#!/usr/bin/env python3

from setuptools import setup

setup(name='ultimate_ttt',
      version='0.1',
      description='Game engine for Ultimate TicTacToe games',
      author='Bharat Reddy',
      author_email='me@bharatreddy.com',
      url='https://github.com/socialgorithm/ultimate-ttt-py',
      packages=['ultimate_ttt'],
	  setup_requires=['pytest-runner'],
	  tests_require=['pytest']
     )

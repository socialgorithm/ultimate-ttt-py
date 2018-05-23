#!/usr/bin/env python3

from setuptools import setup


with open('README.rst') as f:
    readme = f.read()

setup(name='ultimate_ttt',
      version='1.3',
      description='Game engine and sample player for Ultimate TicTacToe games',
      long_description=readme,
      author='socialgorithm',
      author_email='hello@socialgorithm.org',
      url='https://github.com/socialgorithm/ultimate-ttt-py',
      packages=['engine','players'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      download_url="https://github.com/socialgorithm/ultimate-ttt-py/archive/1.3.tar.gz",
      keywords='ultimate tictactoe uttt ultimate-ttt'
)

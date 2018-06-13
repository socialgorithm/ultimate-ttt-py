=====================================================================
Ultimate TicTacToe - Python Player & Game Engine - Contribution Guide
=====================================================================

Pull Requests
_____________

To make a contribution, please fork this repository and open a pull request. We are grateful for anything that can be
improved for the students taking part in our hackathons.

In general, any new functionality or player should be tested to ensure it is behaving as expected.

Running Tests
-------------

You (and Travis CI) can ensure our tests pass by running :code:`./setup.py test` in the root directory. Keep it that way!

Pushing New Versions
--------------------

To push a new version:

1. Update the :code:`version` string and :code:`download_url` in the :code:`setup.py` file to the new version
1. Update the documentation
  1. `cd docs`
  1. `sphinx-apidoc -o source/ ../engine`
  1. `make html`
1. Create a git tag for the new version and push that

.. Images and Links

.. |Travis| image:: https://travis-ci.org/socialgorithm/ultimate-ttt-py.svg?branch=master
    :target: https://travis-ci.org/socialgorithm/ultimate-ttt-py
.. |PyPI| image:: https://badge.fury.io/py/ultimate_ttt.svg
    :target: https://badge.fury.io/py/ultimate_ttt
.. |Coverage| image:: https://coveralls.io/repos/github/socialgorithm/ultimate-ttt-py/badge.svg?branch=master
    :target: https://coveralls.io/github/socialgorithm/ultimate-ttt-py?branch=master

.. _Ultimate TicTacToe: https://uttt.socialgorithm.org
.. _Ultimate TTT Docs: https://socialgorithm.org/ultimate-ttt-docs
.. _API Reference: https://ultimate-ttt-py.readthedocs.io/en/latest/
.. _Contribution Guide: https://github.com/socialgorithm/ultimate-ttt-py/blob/master/CONTRIBUTING.rst

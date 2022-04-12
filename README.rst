========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions| |requires|
        | |coveralls| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-matrix/badge/?style=flat
    :target: https://python-matrix.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/ionelmc/python-matrix/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/ionelmc/python-matrix/actions

.. |requires| image:: https://requires.io/github/ionelmc/python-matrix/requirements.svg?branch=main
    :alt: Requirements Status
    :target: https://requires.io/github/ionelmc/python-matrix/requirements/?branch=main

.. |coveralls| image:: https://coveralls.io/repos/ionelmc/python-matrix/badge.svg?branch=main&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/ionelmc/python-matrix

.. |codecov| image:: https://codecov.io/gh/ionelmc/python-matrix/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://codecov.io/github/ionelmc/python-matrix

.. |version| image:: https://img.shields.io/pypi/v/matrix.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/matrix

.. |wheel| image:: https://img.shields.io/pypi/wheel/matrix.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/matrix

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/matrix.svg
    :alt: Supported versions
    :target: https://pypi.org/project/matrix

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/matrix.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/matrix

.. |commits-since| image:: https://img.shields.io/github/commits-since/ionelmc/python-matrix/v2.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/ionelmc/python-matrix/compare/v2.0.1...main



.. end-badges

Generic matrix generator.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install matrix

You can also install the in-development version with::

    pip install https://github.com/ionelmc/python-matrix/archive/main.zip


Documentation
=============


https://python-matrix.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

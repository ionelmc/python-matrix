========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-matrix/badge/?style=flat
    :target: https://readthedocs.org/projects/python-matrix
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/ionelmc/python-matrix.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/ionelmc/python-matrix

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/ionelmc/python-matrix?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/ionelmc/python-matrix

.. |requires| image:: https://requires.io/github/ionelmc/python-matrix/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/ionelmc/python-matrix/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/ionelmc/python-matrix/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/ionelmc/python-matrix

.. |codecov| image:: https://codecov.io/github/ionelmc/python-matrix/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/ionelmc/python-matrix

.. |version| image:: https://img.shields.io/pypi/v/matrix.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/matrix

.. |commits-since| image:: https://img.shields.io/github/commits-since/ionelmc/python-matrix/v2.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/ionelmc/python-matrix/compare/v2.0.1...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/matrix.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/matrix

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/matrix.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/matrix

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/matrix.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/matrix


.. end-badges

Generic matrix generator.

* Free software: BSD license

Installation
============

::

    pip install matrix

Documentation
=============

https://python-matrix.readthedocs.io/

Development
===========

To run the all tests run::

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

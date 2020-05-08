========
Overview
========

Certificate management utilities with Vault backend

* Free software: Apache Software License 2.0

Installation
============

::

    pip install knox

You can also install the in-development version with::

    pip install git+ssh://git@git.8x8.com/ljohnson/knox.git@master

Documentation
=============


https://knox.readthedocs.io/


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

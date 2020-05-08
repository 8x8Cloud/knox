========
Overview
========

**TL;DR;** A set of certificate management utilities using a default Vault backend.

* Free software: Apache Software License 2.0

What is knox
============

The name is derived from "Fort Knox" the safest place to store valuables in history. At least that is the myth. This tool or set of utilities is explicitly for managing TLS certificates including metadata about them and storing it in a backend.

Installation
============

::

    pip install knox

You can also install the in-development version with::

    pip install git+ssh://git@github.com/8x8cloud/knox.git@develop

Documentation
=============


https://knox.readthedocs.io/


Development
===========

This project was initialized using a very cool python project templating tool called `cookiecutter-pylibrary <https://github.com/ionelmc/cookiecutter-pylibrary>`_ from `Ionel Cristian Mărieș <https://github.com/ionelmc>`_.

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

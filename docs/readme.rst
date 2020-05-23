.. warning::

    This python project is not fully baked yet. When a full major version is bumped we will consider it functional. Until then enjoy reading the docs.

.. start-badges

.. raw:: html

    <p align="center">
        <!--
        <a href="https://pypi.python.org/pypi/knox"><img alt="Pypi version" src="https://img.shields.io/pypi/v/knox.svg"></a>
        -->
        <a href="https://pypi.python.org/pypi/knox"><img alt="Python versions" src="https://img.shields.io/badge/python-3.5%2B%20%7C%20PyPy-blue.svg"></a>
        <a href="https://knox.readthedocs.io/en/stable/index.html"><img alt="Documentation" src="https://img.shields.io/readthedocs/knox.svg"></a>
        <a href="https://travis-ci.org/8x8Cloud/knox"><img alt="Build status" src="https://img.shields.io/travis/8x8Cloud/knox/develop.svg"></a>
        <!--
        <a href="https://codecov.io/gh/8x8Cloud/knox/branch/master"><img alt="Coverage" src="https://img.shields.io/codecov/c/github/8x8Cloud/knox/master.svg"></a>
        <a href="https://www.codacy.com/app/delgan-py/knox/dashboard"><img alt="Code quality" src="https://img.shields.io/codacy/grade/4d97edb1bb734a0d9a684a700a84f555.svg"></a>
        -->
        <a href="https://github.com/8x8Cloud/knox/blob/develop/LICENSE"><img alt="License" src="https://img.shields.io/github/license/8x8Cloud/knox.svg"></a>
    </p>
.. end-badges


.. note::

    **TL;DR;** A set of certificate management utilities using a default Vault backend.

.. image:: knox-icon.png


.. include:: ../README.md

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




.. _Travis-CI: http://travis-ci.org/
.. _Tox: https://tox.readthedocs.io/en/latest/
.. _Sphinx: http://sphinx-doc.org/
.. _Coveralls: https://coveralls.io/
.. _ReadTheDocs: https://readthedocs.org/
.. _Setuptools: https://pypi.org/project/setuptools
.. _Pytest: http://pytest.org/
.. _AppVeyor: http://www.appveyor.com/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _Nose: http://nose.readthedocs.org/
.. _isort: https://pypi.org/project/isort
.. _bumpversion: https://pypi.org/project/bumpversion
.. _Codecov: http://codecov.io/
.. _Landscape: https://landscape.io/
.. _Scrutinizer: https://scrutinizer-ci.com/
.. _Codacy: https://codacy.com/
.. _CodeClimate: https://codeclimate.com/
.. _`requires.io`: https://requires.io/

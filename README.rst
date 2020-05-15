===========
Knox v0.0.4
===========

**TL;DR;** A set of certificate management utilities using a default Vault backend.

* Free software: Apache Software License 2.0

What is knox
============

The name is derived from "Fort Knox" the safest place to store valuables in history. At least that is the myth. This tool or set of utilities is explicitly for managing TLS certificates including metadata about them and storing it in a backend.

Primary components used are Python, Hashicorp Vault, Let's Encrypt and certbot.

`Let’s Encrypt <https://letsencrypt.org>`_ is a certificate authority managed by the `Internet Security Research Group (ISRG) <https://www.abetterinternet.org/about/>`_. It utilizes the `Automated Certificate Management Environment (ACME) <https://github.com/ietf-wg-acme/acme/>`_ to automatically deploy free SSL certificates that are trusted by nearly all major browsers. `The certificate compatibility list can be found here <https://letsencrypt.org/docs/certificate-compatibility/>`_. Lets Encrypt has revolutionized the distribution of certificates for public facing servers.

`Hashicorp Vault <https://www.vaultproject.io/>`_ is a tool for storing secrets. It has a `PKI Secret Engine <https://www.vaultproject.io/docs/secrets/pki/index.html>`_ backend which allows to use it as a certificate authority in an internal public key infrastructure deployment. Until now, Vault is best suited for issuing private certificates.

Let's Encrypt and Hashicorp Vault are complementary in certificate management.

Installation
============

::

    pip install knox

You can also install the in-development version with::

    pip install git+ssh://git@github.com/8x8cloud/knox.git@develop

Or run it as a container::

    docker run 8x8cloud/knox


Metadata
========

Knox will store the certificate body, in its entirety, along with metadata related to the details of the certificate. The data will be organized and retreived using a tree struction mimicking the DNS naming heirarchy.

Tree Structure::

    certififcates:
    ├── com
    │      └── example
    │       └── cloud
    │           ├── acceptance
    │           ├── production
    │           └── staging
    ├── internal
    │   └── example
    └── net
        └── example

As a result the host name www.example.com storage path will be /com/example/www

Additional data will be stored with the body of the certificates. A jinja template will be provided. Although the cert body and cert data will have alternate RBAC rules for accessing. Below is a sample::

    {
        "cert_info":
        {
            "subject":
            {
                "common_name": "www.example.com",
                "alt_names": ["www.example.com", "example.internal"],
                "business_category": "private org",
                "business_country": "US",
                "business_state": "Delaware",
                "organization": "Example, Inc."
            },
            "issuer":
            {
                "country": "US",
                "organization": "DgigCert, Inc.",
                "organization_unit": "www.digicert.com",
                "common_name": "DigiCert SHA2 EXtended Validation Server CA"
            },
            "validity":
            {
                "not_before": "2019-07-17T22:26:38.493580484Z",
                "not_after": "2021-07-17T22:26:38.493580484Z"
            }
        },

        "cert_body":
        {
            "private": "REDACTED",
            "chain": "REDACTED",
            "public": "REDACTED"
        }
    }





Documentation
=============


https://knox.readthedocs.io/


Development
===========

This project was initialized using a very cool python project templating tool called `cookiecutter-pylibrary <https://github.com/ionelmc/cookiecutter-pylibrary>`_ from `Ionel Cristian Mărieș <https://github.com/ionelmc>`_. Definitely check it out to see all the tools available and good usage docs.

To execute everything run::

  tox

To see all the tox environments::

  tox -l

To only build the docs::

  tox -e docs

To build and verify that the built package is proper and other code QA checks::

  tox -e check

To update `Travis CI <https://travis-ci.org>`_ configuration::

    tox -e bootstrap


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

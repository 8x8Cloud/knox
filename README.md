
What is Knox v0.0.10
====================

The name is derived from "Fort Knox" the safest place to store valuables in history. At least that is the myth. This tool or set of utilities is explicitly for managing TLS certificates including metadata about them and storing it in a backend.

Primary components used are Python, Hashicorp Vault, Let's Encrypt and certbot.

[Let’s Encrypt](<https://letsencrypt.org>) is a certificate authority managed by the [Internet Security Research Group (ISRG)](<https://www.abetterinternet.org/about/>). It utilizes the [Automated Certificate Management Environment (ACME)](<https://github.com/ietf-wg-acme/acme/>) to automatically deploy free SSL certificates that are trusted by nearly all major browsers. [The certificate compatibility list can be found here](<https://letsencrypt.org/docs/certificate-compatibility/>). Lets Encrypt has revolutionized the distribution of certificates for public facing servers.

[Hashicorp Vault](<https://www.vaultproject.io/>) is a tool for storing secrets. It has a [PKI Secret Engine](<https://www.vaultproject.io/docs/secrets/pki/index.html>) backend which allows to use it as a certificate authority in an internal public key infrastructure deployment. Until now, Vault is best suited for issuing private certificates.

Let's Encrypt and Hashicorp Vault are complementary in certificate management.

Installation
============

To get started::

    pip install knox

You can also install the in-development version with::

    pip install git+ssh://git@github.com/8x8cloud/knox.git@develop

Or run it as a container::

    docker run 8x8cloud/knox

See [Dynaconf](https://dynaconf.readthedocs.io/en/latest/) for how the configuration is read in. At its simplest just add environment variables into a `.env` file.


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

This project was initialized using a very cool python project templating tool called [cookiecutter-pylibrary](https://github.com/ionelmc/cookiecutter-pylibrary) from [Ionel Cristian Mărieș](https://github.com/ionelmc). Definitely check it out to see all the tools available and good usage docs.

To execute everything run::

	tox

To see all the tox environments::

	tox -l

To only build the docs::

	tox -e docs

To build and verify that the built package is proper and other code QA checks::

	tox -e check

To update [Travis CI](https://travis-ci.org) configuration::

	tox -e bootstrap


You will need a [Vault](https://hub.docker.com/_/vault) server running locally::

	>docker run \
	--cap-add=IPC_LOCK \
	-p 8201:8201 \
	-p 8200:8200 \
	-e 'VAULT_DEV_ROOT_TOKEN_ID=knox' \
	-d --name=dev-vault \
	vault

	>docker ps
	CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                              NAMES
	d89fbfd340c3        vault               "docker-entrypoint.s…"   5 hours ago         Up 5 hours          0.0.0.0:8200-8201->8200-8201/tcp   dev-vault

Set the token ID and container name to your preferences.
Verify you can talk to vault using the vault cli::

	>export VAULT_ADDR=http://0.0.0.0:8200
	>export VAULT_TOKEN=knox

	>vault status

	Key             Value
	---             -----
	Seal Type       shamir
	Initialized     true
	Sealed          false
	Total Shares    1
	Threshold       1
	Version         1.4.1
	Cluster Name    vault-cluster-31da8ea9
	Cluster ID      043bfc14-09b1-6033-1c3b-8aeace3adc60
	HA Enabled      false

Update your knox configuration using `.env`::

	ENVVAR_PREFIX_FOR_DYNACONF=KNOX

	KNOX_TEMP=/tmp
	KNOX_STORE_ENGINE=vault
	KNOX_VAULT_URL=http://0.0.0.0:8200
	KNOX_VAULT_TOKEN="knox"
	KNOX_VAULT_MOUNT="certificates"
	KNOX_FILE_HOME=./test




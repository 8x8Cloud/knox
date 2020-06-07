"""
Apache Software License 2.0

Copyright (c) 2020, 8x8, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -m knox` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``knox.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``knox.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import sys

import click
import pkg_resources
from loguru import logger

from .certificate import Cert  # noqa: F401
from .config import Conf
from .knox import Knox


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.version_option(version=pkg_resources.get_distribution('knox').version)
@click.pass_context
@logger.catch()
def cli(ctx, debug):
    """Utilities for managing and storing TLS certificates using backing store (Vault)."""
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    logger.remove()
    if debug:
        ctx.obj['LOG_LEVEL'] = 'DEBUG'
        logger.add(sys.stdout, format="{time} {level: >9} {level.icon} {message}", filter=Conf.log_filter, level="DEBUG", colorize=True)
        logger.info(f' Log level set to {ctx.obj["LOG_LEVEL"]}')
    else:
        ctx.obj['LOG_LEVEL'] = 'WARNING'
        logger.add(sys.stderr, format="{time} {level: >9} {level.icon} {message}", filter=Conf.log_filter, level="WARNING", colorize=True)


@cli.group(no_args_is_help=True)
@click.option("--type", "-t", type=click.Choice(['PEM', 'DER', 'PFX'], case_sensitive=True), default='PEM', show_default=True)
@click.option("--pub", type=click.File("r"), help="Public key file")
@click.option("--chain", type=click.File("r"), help="Intermediate chain")
@click.option("--key", type=click.File("r"), help="Private key file")
@click.pass_context
@logger.catch()
def cert(ctx, type, pub, chain, key):
    """Certificate utilities.

    NAME is the common name for the certificate. i.e. www.example.com
    """
    ctx.obj['CERT_PUB'] = pub
    ctx.obj['CERT_CHAIN'] = chain
    ctx.obj['CERT_KEY'] = key
    ctx.obj['CERT_TYPE'] = type


@cert.command(no_args_is_help=True)
@click.argument("name")
@click.pass_context
@logger.catch()
def save(ctx, name):
    """Store an existing certificate
    """
    ctx.obj['CERT_NAME'] = name
    pub = ctx.obj['CERT_PUB']
    key = ctx.obj['CERT_KEY']
    chain = ctx.obj['CERT_CHAIN']
    certtype = ctx.obj['CERT_TYPE']

    knox = Knox(ctx.obj['LOG_LEVEL'])
    certificate = Cert(knox.settings, common_name=name)
    certificate.load(pub=pub.name,
                     key=key.name,
                     chain=chain.name,
                     certtype=certtype)
    knox.store.save(certificate)


@cert.command(no_args_is_help=True)
@click.argument("name")
@click.pass_context
@logger.catch()
def get(ctx, name):
    """Retrieve an existing certificate for a given common name from the store
    """
    ctx.obj['CERT_NAME'] = name
    knox = Knox(ctx.obj['LOG_LEVEL'])
    certificate = Cert(knox.settings, common_name=name)
    certificate.type = ctx.obj['CERT_TYPE']
    certificate = knox.store.get(certificate.store_path(), name=name, type=certificate.type)
    with open(certificate.name+"-pub.pem", "w") as pubf:
        pubf.write(certificate.body['public'])
    with open(certificate.name+"-key.pem", "w") as keyf:
        keyf.write(certificate.body['private'])
    with open(certificate.name+"-chain.pem", "w") as chainf:
        chainf.write(certificate.body['chain'])


@cert.command(no_args_is_help=True)
@click.argument("name")
@click.pass_context
@logger.catch()
def gen(ctx, name):
    """Create and store a new certificate for a given common name
    """
    ctx.obj['CERT_NAME'] = name

    knox = Knox(ctx.obj['LOG_LEVEL'])
    certificate = Cert(knox.settings, common_name=name)
    certificate.generate()
    knox.store.save(certificate)


@cli.command(no_args_is_help=True)
@click.option("-f", "--find", help="Find certificate by common name")
@click.argument("name")
@click.pass_context
@logger.catch()
def store(ctx, find, name) -> dict:
    """Store commands. Given a certificate NAME perform the store operation.

    NAME can be similar to a full file path or the certificates common name.
    i.e. www.example.com becomes /com/example/www/www.example.com when stored.

    """
    ctx.obj['STORE_FIND'] = find
    knox = Knox(ctx.obj['LOG_LEVEL'])
    if find:
        certificate = knox.store.find(Cert.to_store_path(name), name=name)  # noqa F841
        # save certificate_public_key.pem
        # save certificate_private_key.pem
        # save certificate_chain.pem

    return ctx


def main():
    cli(prog_name="knox", obj={})


if __name__ == "__main__":
    main()

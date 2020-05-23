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


Entrypoint module, in case you use `python -mknox`.


Why does this file exist, and why __main__? For more info, read:

- https://www.python.org/dev/peps/pep-0338/
- https://docs.python.org/2/using/cmdline.html#cmdoption-m
- https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""
import sys

import click
from loguru import logger

from .certificate import Cert  # noqa: F401
from .config import Conf
from .knox import Knox

logger.remove()
logger.add(sys.stderr, format="{time} {level} {message}", filter=Conf.log_filter, level="INFO")

knox = Knox()
logger.info(f'Knox loaded {knox.conf.version}')


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
@logger.catch()
def cli(ctx, debug) -> dict:
    """Utilities for managing and storing TLS certificates using backing store (Vault)."""
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    if debug:
        knox.conf.log_level = "DEBUG"
        logger.info(f'Log level set to {knox.conf.log_level}')


@cli.command(no_args_is_help=True)
@click.option("--type", "-t", type=click.Choice(['PEM', 'DER'], case_sensitive=True), default='PEM', show_default=True)
@click.option("--save/--read", default=True, help="Save or Read to/from the store")
@click.option("--pub", type=click.File("r"), help="Public key file")
@click.option("--chain", type=click.File("r"), help="Intermediate chain")
@click.option("--key", type=click.File("r"), help="Private key file")
@click.argument("name")
@click.pass_context
@logger.catch()
def cert(ctx, type, save, pub, chain, key, name) -> dict:
    """Certificate utilities.

    NAME is the common name for the certificate. i.e. www.example.com
    """

    ctx.obj['CERT_PUB'] = pub
    ctx.obj['CERT_CHAIN'] = chain
    ctx.obj['CERT_KEY'] = key
    ctx.obj['CERT_TYPE'] = type
    ctx.obj['CERT_SAVE'] = save
    ctx.obj['CERT_NAME'] = name

    certificate = Cert(name)
    if save:
        certificate.load(pub=pub.name,
                         key=key.name,
                         chain=chain.name,
                         certtype=Cert.PEM)
        knox.store.save(certificate)
    else:
        certificate = knox.store.get(certificate.store_path(), name=name)
        logger.debug(f'Found {certificate.name}')
        with open(certificate.name+"-pub.pem", "w") as pubf:
            pubf.write(certificate.body['public'])
        with open(certificate.name+"-key.pem", "w") as keyf:
            keyf.write(certificate.body['private'])
        with open(certificate.name+"-chain.pem", "w") as chainf:
            chainf.write(certificate.body['chain'])

    return ctx


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
    if find:
        certificate = knox.store.find(Cert.to_store_path(name), name=name)  # noqa F841
        # save certificate_public_key.pem
        # save certificate_private_key.pem
        # save certificate_chain.pem

    return ctx


if __name__ == "__main__":
    cli(prog_name="knox", obj={})

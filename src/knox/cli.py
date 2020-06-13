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
limitations under the License. """
import csv
import json
import sys

import click
import pkg_resources
from loguru import logger

from .certificate import Cert  # noqa: F401
from .config import Conf
from .knox import Knox


@click.group()
@click.option("--log", "-l",
              type=click.Choice(['TRACE',
                                 'DEBUG',
                                 'INFO',
                                 'SUCCESS',
                                 'WARNING',
                                 'ERROR',
                                 'CRITICAL']),
              default='INFO',
              show_default=True,
              help="Sets the level of logging displayed")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Display log output to console")
@click.version_option(version=pkg_resources.get_distribution('knox').version)
@click.pass_context
@logger.catch()
def cli(ctx, verbose: bool = False, log: str = 'INFO'):
    """Utilities for managing and storing TLS certificates using backing store (Vault)."""
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose
    ctx.obj['LOG_LEVEL'] = log
    logger.remove()
    if verbose:
        logger.add(sys.stdout,
                   format="{time} {level: >9} {level.icon} {message}",
                   filter=Conf.log_filter,
                   level=f"{log}",
                   colorize=True)
        logger.info(f' Log level set to {ctx.obj["LOG_LEVEL"]}')
    else:
        logger.add(sys.stderr,
                   format="{time} {level: >9} {level.icon} {message}",
                   filter=Conf.log_filter,
                   level=f"{log}",
                   colorize=True)


@cli.group(no_args_is_help=True)
@click.option("--type", "-t",
              type=click.Choice(['PEM', 'DER', 'PFX'], case_sensitive=False),
              default='PEM',
              show_default=True)
@click.option("--pub", help="Public key file")
@click.option("--chain", help="Intermediate chain")
@click.option("--key", help="Private key file")
@click.pass_context
@logger.catch()
def cert(ctx, pub: str, key: str, type: str = 'PEM', chain: str = None):
    """Certificate utilities.

    NAME is the common name for the certificate. i.e. www.example.com
    """
    ctx.obj['CERT_PUB'] = pub
    ctx.obj['CERT_CHAIN'] = chain
    ctx.obj['CERT_KEY'] = key
    ctx.obj['CERT_TYPE'] = type.upper()


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
    certificate.load(pub=pub,
                     key=key,
                     chain=chain,
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


@cli.group(no_args_is_help=True)
@click.pass_context
def store(ctx) -> dict:
    """Store commands. Given a certificate NAME perform the store operation."""
    pass


@store.command(no_args_is_help=True)
@click.option("--file", "-f", help="Output file, default stdout")
@click.option("--output", "-o",
              type=click.Choice(['JSON', 'CSV'], case_sensitive=False),
              default='JSON',
              show_default=True,
              help="Type of output")
@click.argument("name")
@click.pass_context
@logger.catch()
def find(ctx, name, file: str = 'stdout', output: str = 'JSON') -> dict:
    """Given a certificate NAME pattern search the store.

    NAME can be similar to a full file path or the certificates common name.
    i.e. www.example.com becomes /com/example/www/www.example.com when stored.
    Supports wild cards. *.example.com

    """
    ctx.obj['STORE_FIND_NAME'] = name
    ctx.obj['STORE_FIND_OUTPUT'] = output
    ctx.obj['STORE_FIND_OUTFILE'] = file
    knox = Knox(ctx.obj['LOG_LEVEL'])
    if name:
        results = knox.store.find(pattern=name)  # noqa F841
        handle = open(file, 'w') if file else sys.stdout
        if output == 'JSON':
            handle.write(json.dumps(results, indent=4))
        else:
            csv_writer = csv.writer(handle)
            count = 0
            for rec in results:
                if count == 0:
                    header = rec.keys()
                    csv_writer.writerow(header)
                    count += 1
                csv_writer.writerow(rec.values())

        handle.close()

    return ctx


def main():
    cli(prog_name="knox", obj={})


if __name__ == "__main__":
    main()

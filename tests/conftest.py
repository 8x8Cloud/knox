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
limitations under the License."""
import knox
import pytest
import pathlib
import sys
import requests
import hvac
import json
import datetime
import os
import cryptography.x509.base

from dynaconf import settings

from requests.exceptions import ConnectionError
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dh, rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends.openssl import backend as openssl_backend
from .hazmat.primitives.fixtures_rsa import RSA_KEY_2048

from click import Context, Command

@pytest.fixture()
def backend():
    return openssl_backend


class KnoxTestFixtureData:
    """Test setup object"""
    _cert: cryptography.x509.base.Certificate
    _key: cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey
    _knox: knox.Knox
    _approleid: str
    _approlesecret: str = "supersecret"

    def __init__(self):
        """Constructor for KnoxTextFixtures"""

    def initialize(self) -> None:
        cmd = Command
        ctx = Context(cmd, obj={'VERBOSE': False,
                                'LOG_LEVEL': "INFO",
                                'ADMIN_MODE': False
                                })
        settings.VAULT_APPROLE = self._approleid
        settings.VAULT_SECRET_ID = self._approlesecret
        self._knox = knox.Knox(ctx)

    @property
    def approleid(self) -> str:
        return self._approleid

    @approleid.setter
    def approleid(self, value: str) -> None:
        self._approleid = value

    @property
    def approlesecret(self) -> str:
        return self._approlesecret

    @approlesecret.setter
    def approlesecret(self, value: str) -> None:
        self._approlesecret = value

    def knox(self) -> knox.Knox:
        return self._knox

    def gen_cert(self):
        issuer_private_key = RSA_KEY_2048.private_key(openssl_backend)
        subject_private_key = RSA_KEY_2048.private_key(openssl_backend)

        not_valid_before = datetime.datetime(2002, 1, 1, 12, 1)
        not_valid_after = datetime.datetime(2030, 12, 31, 8, 30)

        builder = (
            x509.CertificateBuilder()
                .serial_number(777)
                .issuer_name(
                    x509.Name(
                        [
                            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                            x509.NameAttribute(
                                NameOID.STATE_OR_PROVINCE_NAME, "Texas"
                            ),
                            x509.NameAttribute(NameOID.LOCALITY_NAME, "Austin"),
                            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "PyCA"),
                            x509.NameAttribute(
                                NameOID.COMMON_NAME, "cryptography.io"
                            ),
                        ]
                    )
                )
                .subject_name(
                x509.Name(
                        [
                            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                            x509.NameAttribute(
                                NameOID.STATE_OR_PROVINCE_NAME, "Texas"
                            ),
                            x509.NameAttribute(NameOID.LOCALITY_NAME, "Austin"),
                            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "PyCA"),
                            x509.NameAttribute(
                                NameOID.COMMON_NAME, "cryptography.io"
                            ),
                        ]
                    )
                )
                    .public_key(subject_private_key.public_key())
                    .add_extension(
                    x509.BasicConstraints(ca=False, path_length=None),
                    True,
                )
                    .add_extension(
                    x509.SubjectAlternativeName([x509.DNSName("cryptography.io")]),
                    critical=False,
                )
                    .not_valid_before(not_valid_before)
                    .not_valid_after(not_valid_after)
            )

        cert = builder.sign(issuer_private_key, hashes.SHA256(), openssl_backend)

        self._cert = cert
        self._key = issuer_private_key
        return cert

    def cert_pub(self):
        return self._cert.public_bytes(encoding=serialization.Encoding.PEM)

    def cert_key(self):
        return self._key.private_bytes(encoding=serialization.Encoding.PEM,
                                       format=serialization.PrivateFormat.TraditionalOpenSSL,
                                       encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"))


@pytest.fixture(scope="session")
def ktfdata() -> KnoxTestFixtureData:
    knoxtestfixturedata = KnoxTestFixtureData()
    return knoxtestfixturedata


def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope="session")
def vault_container(docker_ip, docker_services):

    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("vault", 8200)
    vaulturl = f"http://{docker_ip}:{port}"
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(vaulturl)
    )

    client = hvac.Client(url=vaulturl, token='knox')

    return client


@pytest.fixture(scope="session")
def vault_initialized(vault_container, docker_ip, ktfdata):
    headers = {'Content-Type': 'application/json', 'X-Vault-Token': 'knox'}

    policies = vault_container.sys.list_policies()['data']['policies']

    cwd = pathlib.Path.cwd()
    if cwd.name.lower() != "tests":
        datapath = f"{cwd}/tests/data"
    else:
        datapath = f"{cwd}/data"

    if "admin-policy" not in policies:
        # Apply Vault policies
        for filename in os.listdir(path=f"{datapath}"):
            if filename.startswith('cert_'):
                (policyname, ext) = os.path.splitext(filename)
                with open(f"{datapath}/{filename}", mode="r") as contents:
                    vault_container.sys.create_or_update_policy(
                        name=policyname[5:],
                        policy=contents.read(),
                    )

    # Enable Vault AppRole Auth Method
    authmethods = vault_container.sys.list_auth_methods()
    if "approle" not in authmethods:
        vault_container.sys.enable_auth_method(
           method_type='approle',
        )

    secrets_engines = vault_container.sys.list_mounted_secrets_engines()

    if "certificate" not in secrets_engines:
        # Enable Secrets engine
        vault_container.sys.enable_secrets_engine(
           backend_type='kv',
           path='certificate',
        )

    # Create Approle entity and associated secret
    with open(f"{datapath}/approle-role-certificatestore.json", mode="r") as approlejson:
        requests.post(url=f"http://{docker_ip}:8200/v1/auth/approle/role/certificatestore", headers=headers,
                      data=approlejson.read())
        response = requests.get(url=f"http://{docker_ip}:8200/v1/auth/approle/role/certificatestore/role-id",
                                headers=headers)
        approleid = json.loads(response.content.decode('utf-8'))['data']['role_id']
        ktfdata.approleid = approleid

    requests.post(url=f"http://{docker_ip}:8200/v1/auth/approle/role/certificatestore/custom-secret-id",
                  headers=headers, data='{"secret_id": "supersecret"}')
    approlesecret = "supersecret"
    ktfdata.approlesecret = approlesecret

    vault_container.auth.approle.login(approleid, approlesecret)

    client = hvac.Client(url=f"http://{docker_ip}:8200", token='knox')

    ktfdata.initialize()

    return client

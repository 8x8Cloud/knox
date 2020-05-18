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
import ast
import json
from binascii import hexlify

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding
from jinja2 import Environment
from jinja2 import FileSystemLoader

from ..backend import StoreObject


class Cert(StoreObject):
    """Object representation of a TLS certificate"""
    _body: str  #: String representation of private, chain and public portions of certificate as a map/json
    _info: str  #: Certificate details
    _data: {}  #: Combined body and info string
    _file: object
    _x509: x509

    _common_name: str
    _jinja: Environment

    def __init__(self, common_name) -> None:
        """Constructor for Cert"""
        self._common_name = common_name
        self._body = ""
        self._info = ""
        super().__init__(common_name, self.store_path(), self._body, self._info)
        self._jinja = Environment(loader=FileSystemLoader('templates'))
        self._tmpl_body = self._jinja.get_template('body_template.js')
        self._tmpl_info = self._jinja.get_template('info_template.js')
        self._tmpl_data = self._jinja.get_template('data_template.js')

    def load_x509(self, path: str) -> None:
        """Given path to PEM x509 read in certificate"""
        with open(path, mode='r+', encoding='utf-8') as fp:
            self._file = fp.read()
            self._x509 = x509.load_pem_x509_certificate(bytes(self._file, 'utf-8'), default_backend())
        self._info = ast.literal_eval(self._tmpl_info.render(cert=self))
        self._body = ast.literal_eval(self._tmpl_body.render(cert=self))
        self._data = ast.literal_eval(self._tmpl_data.render(cert=self))
        self._body['cert_body']['public'] = self._file
        self._data['cert_body']['public'] = self._file
        self._common_name = self._data['cert_info']['subject']['commonName']
        self.name = self._common_name
        self.path = self.store_path()

    def subject(self) -> str:
        return json.dumps({attr.oid._name: attr.value for attr in self._x509.subject}, indent=8)

    def issuer(self) -> str:
        return json.dumps({attr.oid._name: attr.value for attr in self._x509.issuer}, indent=8)

    def validity(self) -> str:
        cert = self._x509
        return json.dumps({
            'not_valid_before': cert.not_valid_before.timestamp(),
            'not_valid_after': cert.not_valid_after.timestamp(),
        }, indent=8)

    def key_details(self) -> str:
        cert = self._x509
        public_key = self._x509.public_key()
        key_info = {'size': public_key.key_size}
        if isinstance(public_key, rsa.RSAPublicKey):
            key_type = 'RSA'
        elif isinstance(public_key, dsa.DSAPublicKey):
            key_type = 'DSA'
        elif isinstance(public_key, ec.EllipticCurvePublicKey):
            key_type = 'ECC'
            key_info['curve'] = public_key.curve.name
        else:
            raise ValueError('Invalid key type.')
        key_info['type'] = key_type
        return json.dumps({
            'version': cert.version.name,
            'fingerprint_sha256': hexlify(cert.fingerprint(hashes.SHA256())).decode(),
            'serial_number': cert.serial_number,
            'key': key_info
        }, indent=8)

    def store_path(self) -> str:
        """Generate a backend store path based on the certificates common name
        www.example.com becomes /com/example/www

            :return: str
        """
        domainsplit = self._common_name.split('.')
        return "/"+"/".join(reversed(domainsplit))

    def __str__(self) -> str:
        return json.dumps(self._data, indent=4)

    def private(self) -> str:
        return ""

    def chain(self) -> str:
        return ""

    def public(self) -> str:
        return self._x509.public_bytes(Encoding.PEM).decode('utf-8').replace('\n', '')

    def info(self) -> str:
        return json.dumps(self._info['cert_info'], indent=4)

    def body(self) -> str:
        return json.dumps(self._body['cert_body'], indent=4)

    @property
    def data(self) -> str:
        """Content to persist, typically JSON"""
        return self._data

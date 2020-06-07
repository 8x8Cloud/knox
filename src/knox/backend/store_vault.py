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
import json

import hvac
import requests
from dynaconf import LazySettings
from loguru import logger

from .store_engine import StoreEngine
from .store_object import StoreObject


class VaultClient:
    """Client commands not available via hvac"""

    __vault_client: hvac.Client

    __headers = {'Content-Type': 'application/json',
                 'X-Vault-Token': ''}
    __url: str       #: Vault server URL
    __token: str     #: Auth token
    __approle: str   #: Application Role ID
    __secretid: str  #: Application Role Secret ID
    __mount: str     #: Engine mount path
    __mounts: json

    def __init__(self, settings: LazySettings) -> None:
        """Constructor for VaultRESTClient"""
        self.__url = settings.VAULT_URL
        self.__approle = settings.VAULT_APPROLE
        self.__secretid = settings.VAULT_SECRET_ID
        self.__mount = settings.VAULT_MOUNT

    def open(self) -> bool:

        """Get temp token for approle"""
        res = self._post('/v1/auth/approle/login', f'{{"role_id": "{self.__approle}", "secret_id": "{self.__secretid}"}}')
        self.__token = res['auth']['client_token']
        self.__headers['X-Vault-Token'] = self.__token

        self.__vault_client = hvac.Client(url=self.__url)
        self.__vault_client.auth_approle(role_id=self.__approle, secret_id=self.__secretid, use_token=False)

        return self.__vault_client.is_authenticated()

    def url(self) -> str:
        return self.__url

    def mount(self) -> str:
        return self.__mount

    def logout(self) -> bool:
        return self.__vault_client.logout()

    def _get(self, path: str) -> json:
        """GET REST API wrapper method

            :param path: Vault API to query
            :type path: String
            :return: JSON paylod
        """
        try:
            response = requests.get(self.__url+path, headers=self.__headers)
            response.raise_for_status()

            return json.loads(response.content.decode('utf-8'))

        except requests.exceptions.HTTPError as errh:
            logger.error(f'Http Error: {errh}')
        except requests.exceptions.ConnectionError as errc:
            logger.error(f'Error Connecting: {errc}')
        except requests.exceptions.Timeout as errt:
            logger.error(f'Timeout Error: {errt}')
        except requests.exceptions.RequestException as err:
            logger.error(f'Error: {err}')

    def _post(self, path: str, data: json) -> requests.Response:
        """POST REST API wrapper method

            :param path: Vault API to change or create
            :type path: String
            :param data: Required request body
            :type data: JSON
            :return: requests.Response object
        """
        try:
            response = requests.post(self.__url+path, headers=self.__headers, data=data)
            response.raise_for_status()

            return json.loads(response.content.decode('utf-8'))

        except requests.exceptions.HTTPError as errh:
            logger.error(f'Http Error: {errh}')
        except requests.exceptions.ConnectionError as errc:
            logger.error(f'Error Connecting: {errc}')
        except requests.exceptions.Timeout as errt:
            logger.error(f'Timeout Error: {errt}')
        except requests.exceptions.RequestException as err:
            logger.error(f'Error: {err}')

    def _put(self, path: str, data: json) -> requests.Response:
        """PUT REST API wrapper method

            :param path: Vault API to change or create
            :type path: String
            :param data: Required request body
            :type data: JSON
            :return: requests.Response object
        """
        try:
            response = requests.put(self.__url+path, headers=self.__headers, data=data)
            response.raise_for_status()

            return response

        except requests.exceptions.HTTPError as errh:
            logger.error(f'Http Error: {errh}')
        except requests.exceptions.ConnectionError as errc:
            logger.error(f'Error Connecting: {errc}')
        except requests.exceptions.Timeout as errt:
            logger.error(f'Timeout Error: {errt}')
        except requests.exceptions.RequestException as err:
            logger.error(f'Error: {err}')

    def get_mounts(self) -> json:
        """Refresh set of mounts from Vault

            :return: JSON
        """
        self.__mounts = self._get("/v1/sys/mounts")
        return self.__mounts

    def new_mount(self, mount: str) -> bool:
        """Will create a vault mount of type k/v V2 if it doesn't exist

            :param mount: Name of the Vault K/V Secret Engine
            :type mount: String
            :return: Boolean
        """
        self.__mounts = self._get("/v1/sys/mounts")
        if mount+"/" not in self.__mounts['data'].keys():
            logger.info(f'Vault mount {self.__url}/v1/sys/mounts/{mount} does not exist, creating')
            self._put(f'/v1/sys/mounts/{mount}', '{"type": "kv-v2"}')
            self.__mounts = self._get("/v1/sys/mounts")
        return mount+"/" in self.__mounts['data'].keys()

    def upsert(self, obj: StoreObject) -> bool:
        client = self.__vault_client
        mp = self.mount()

        try:
            client.secrets.kv.v2.create_or_update_secret(path=obj.path_name + "/cert_body",
                                                         mount_point=mp,
                                                         secret=obj.data['cert_body'])

            client.secrets.kv.v2.create_or_update_secret(path=obj.path_name + "/cert_info",
                                                         mount_point=mp,
                                                         secret=obj.data['cert_info'])
        except Exception as vex:
            logger.error(f'Failed to write StoreObject to Vault {vex}')

        logger.info(f'Successfully stored {obj.path_name}')
        return True

    def read(self, path: str, name: str, type=None) -> tuple:
        client = self.__vault_client
        if type:
            fullpathbody = f'{path}/{name}/{type}/cert_body'
            fullpathinfo = f'{path}/{name}/{type}/cert_info'
        else:
            fullpathbody = f'{path}/{name}/cert_body'
            fullpathinfo = f'{path}/{name}/cert_info'
        certbody = client.secrets.kv.v2.read_secret_version(path=fullpathbody, mount_point=self.mount())
        certinfo = client.secrets.kv.v2.read_secret_version(path=fullpathinfo, mount_point=self.mount())
        return certbody, certinfo


class VaultStoreEngine(StoreEngine):
    """Vault implementation of the StoreEngine interface"""
    __client: VaultClient

    def __init__(self, settings) -> None:
        """Constructor for VaultStoreEngine"""
        super().__init__()
        self._settings = settings
        self.__client = VaultClient(settings)
        logger.debug(f'🔐 Vault backend configuration loaded. {self.__client.url()}')
        if self.initialize():
            logger.debug("🔐 Vault backend initialized.")
        else:
            logger.error(f'🛑 Failed to connect to Vault {self.__client.url()}')
            raise

    def initialize(self) -> bool:
        return self.open()

    def open(self) -> bool:
        """Ensure the vault client is connected"""
        return self.__client.open()

    def close(self) -> bool:
        """Ensure we close the vault connection"""
        return self.__client.logout()

    def __del__(self):
        """When the object is destroyed make sure we close the connection to Vault"""
        return self.close()

    def write(self, obj: StoreObject) -> bool:
        """Given a StoreObject, store it into vault using mount/path/name == body,info

            :param obj: The StoreObject to persist
            :type obj: StoreObject
            :return: bool
        """
        return self.__client.upsert(obj)

    def read(self, path: str, name: str, type=None) -> StoreObject:
        """Using the provided path and name retrieve the data from the store and create a new StoreObject

            :param path: Store path to the object
            :type path: str
            :param name: Name of the object to retrieve
            :type name: str
            :param type: StoreObject type, if known
            :type type: str
            :return: StoreObject
        """
        try:
            certbody, certinfo = self.__client.read(path, name, type)
            cert = StoreObject(name=name,
                               path=path,
                               body=certbody['data']['data'],
                               info=certinfo['data']['data'],
                               type=type)
            cert._data = {'cert_body': certbody['data']['data'], 'cert_info': certinfo['data']['data']}

        except Exception as vex:
            logger.error(f'Failed to read StoreObject /{self.__client.mount()}{path}/{name} {vex}')

        logger.info(f' Successfully read {cert.path_name}')

        return cert

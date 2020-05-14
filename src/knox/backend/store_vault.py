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
import json  # noqa: F401

import hvac
from loguru import logger

from .store_engine import StoreEngine
from .store_object import StoreObject


class VaultStoreEngine(StoreEngine):
    """Vault implementation of the StoreEngine interface"""
    __vault_url: str
    __vault_token: str
    __vault_client: hvac.Client

    def __init__(self, settings) -> None:
        """Constructor for VaultStoreEngine"""
        super().__init__()
        self._settings = settings
        self.__vault_url = settings.VAULT_URL
        self.__vault_token = settings.VAULT_TOKEN
        self.__vault_mount = settings.VAULT_MOUNT
        self.__vault_client = hvac.Client(url=self.__vault_url, token=self.__vault_token)
        logger.debug(f'🔐 Vault backend configuration loaded. {self.__vault_url}')

    def open(self) -> bool:
        return self.__vault_client.is_authenticated()

    def close(self) -> bool:
        return self.__vault_client.close()

    def __del__(self):
        return self.close()

    def write(self, obj: StoreObject) -> bool:
        client = self.__vault_client
        mp = self.__vault_mount
        try:
            client.secrets.kv.v2.create_or_update_secret(path=obj.path + "/" + obj.name + "/cert_body", mount_point=mp,
                                                         secret=obj.body)
            client.secrets.kv.v2.create_or_update_secret(path=obj.path + "/" + obj.name + "/cert_info", mount_point=mp,
                                                         secret=obj.info)
        except Exception:
            logger.error('Failed to write StoreObject to Vault')

    def read(self, path: str, name: str) -> StoreObject:
        client = self.__vault_client
        mp = self.__vault_mount
        obj: StoreObject

        try:
            metadata = client.secrets.kv.v2.read_secret_metadata(path=path + "/" + name, mount_point=mp)
            obj = StoreObject(name, path, metadata['data']['data']['cert_body'], metadata['data']['data']['cert_info'])
        except Exception:
            logger.error(f'Failed to read StoreObject {self.__vault_mount}/{path}/{name}')

        return obj

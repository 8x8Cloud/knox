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
from loguru import logger

from .store_engine import StoreEngine
from .store_file import FileStoreEngine
from .store_object import StoreObject
from .store_vault import VaultStoreEngine


class Store:
    """Abstract class to generalize access to the different stores"""
    _engine: StoreEngine
    _engine_map = {
        'vault': VaultStoreEngine,
        'file': FileStoreEngine
    }

    def __init__(self, settings) -> None:
        """Dynamically load StoreEngine type from .env via Dynaconf
        KNOX_STORE_ENGINE=[vault,file]

        :param settings: Dynaconf LazySettings
        :type settings: dynaconf.LazySettings
        """
        try:
            self._engine = self._engine_map.get(settings.STORE_ENGINE).__call__(settings)
        except Exception:
            logger.error(f'StoreEngineFailure KNOX_STORE_ENGINE={settings.STORE_ENGINE} is invalid. Valid options are {self._engine_map.keys()}')  # noqa: E501
            raise

        self._engine.settings = settings
        logger.debug(f'Loaded {self._engine.__class__}')

    def save(self, obj: StoreObject) -> bool:
        """Save the given object to persistence"""
        return self._engine.write(obj)

    def get(self, path: str, name: str, type=None) -> StoreObject:
        """Given path read object"""
        return self._engine.read(path, name, type)

    def delete(self, path: str, name: str) -> bool:
        """Remove the object from the store"""
        """[TODO 5/13/20] ljohnson implement soft delete and hard deletes"""
        return self._engine.delete(path, name)

    def find(self, path: str, name: str) -> [StoreObject]:
        """Given a path, return collection of all objects"""
        """[TODO 5/13/20] ljohnson implement glob searching /path/**/path2/*"""
        pass

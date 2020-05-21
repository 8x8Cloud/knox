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

from dynaconf.loaders.vault_loader import list_envs
"""
import shortuuid
from dynaconf import settings
from dynaconf.utils.files import SEARCHTREE
from loguru import logger


class Conf:
    """Manage application settings"""
    _version: str
    log_level = "WARNING"

    def __init__(self) -> None:
        """Constructor for Settings"""
        self.log_level = settings.LOG_LEVEL
        self._version = shortuuid.uuid()
        self._settings = settings
        logger.debug(self._settings.dynaconf_banner)
        logger.debug("Learn more at http://github.com/rochacbruno/dynaconf")
        logger.debug(f'dynaconf search tree: {SEARCHTREE}')
        logger.debug(f'dynaconf loaded? {self._settings.configured}')

    @classmethod
    def log_filter(cls, record) -> bool:
        levelno = logger.level(cls.log_level).no
        return record["level"].no >= levelno

    @property
    def version(self) -> str:
        return self._version

    @property
    def settings(self) -> settings:
        return self._settings

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
from loguru import logger


class Conf():
    """Manage application settings"""

    def __init__(self):
        """Constructor for Settings"""
        self.version = shortuuid.uuid()
        self.conf = settings
        logger.debug("loaded constructor Settings()")
        logger.debug(self.conf.dynaconf_banner)
        logger.debug("Learn more at http://github.com/rochacbruno/dynaconf")

    def version(self):
        return self.version

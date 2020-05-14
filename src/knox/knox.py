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
from . import backend as backend
from . import certificate as cert
from . import config as config


class Knox():
    """Composite class for Knox package"""
    _conf: config.Conf
    _store: backend.Store
    _cert: cert.Cert

    def __init__(self, common_name: str) -> None:
        """Constructor for Knox"""
        self._conf = config.Conf()
        self._store = backend.Store(self._conf.settings)
        self._cert = cert.Cert(common_name)

    @property
    def settings(self) -> config.Conf.settings:
        return self._conf.settings

    @property
    def conf(self) -> config.Conf:
        return self._conf

    @property
    def store(self) -> backend.Store:
        return self._store

    @property
    def cert(self) -> cert.Cert:
        return self._cert

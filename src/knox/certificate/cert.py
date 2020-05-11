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


class Cert():
    """Object representation of a TLS certificate"""
    _common_name: str
    _data: str

    def __init__(self, common_name) -> None:
        """Constructor for Cert"""
        self._common_name = common_name

    def store_path(self) -> str:
        """Generate a backend store path based on the certificates common name
        www.8x8.com becomes /com/8x8/www
        """
        domainsplit = self._common_name.split('.')
        return "/".join(reversed(domainsplit))

    def __str__(self) -> str:
        return self._data

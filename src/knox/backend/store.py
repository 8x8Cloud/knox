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


class Store():
    """The persistence strategy for storing the certificates"""

    def __init__(self):
        """Constructor for Store"""

    def open(self):
        """Initialize access to the persistence"""
        pass

    def close(self):
        """Close access to the persistence"""

    def install(self):
        """Ensure the store is configured properly"""
        pass

    def read(self, object):
        """Read from the store"""
        pass

    def write(self, object):
        """Write to the store"""
        pass

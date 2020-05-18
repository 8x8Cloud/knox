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


class DnsEngine():
    """DNS Engine for communicating with DNS providers"""
    provider: str

    def __init__(self) -> str:
        """Constructor for DnsEngine"""

    def validate_provider_credentials(self, provider) -> str:
        """Validate the credentials set for specific DNS provider"""
        pass

    def get_provider_args(self) -> str:
        """Generate certbot commands based on provider name"""
        pass

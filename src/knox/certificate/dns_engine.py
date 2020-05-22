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

import os
from loguru import logger

domain_metadata = {
    "dns": [
        {
            "aws": {
                "required_credentials": [
                    "AWS_ACCESS_KEY_ID",
                    "AWS_SECRET_ACCESS_KEY"
                ],
                "domains": [
                    "acceptance.cloud.8x8.com",
                    "staging.cloud.8x8.com"
                ]
            },
            "cloudflare": {
                "required_crednetials": [
                    "CF_API_EMAIL",
                    "CF_API_KEY"
                ],
                "domains": [
                    "testdomain.8x8.com"
                ]
            },
            "powerdns": {
                "required_credentials": [
                    "PDNS_API",
                    "PDNS_KEY"
                ],
                "domains": [
                    "8x8hosts.internal"
                ]
            }
        }
    ]
}

class DnsEngine():
    """DNS Engine for communicating with DNS providers"""
    provider: str

    def __init__(self, provider) -> str:
        """Constructor for DnsEngine"""
        self._provider = provider

    def validate_provider_credentials(self) -> bool:
        """Validate DNS provider credentials"""
        credentials_list = domain_metadata.get('dns')[0].get(self._provider).get('required_credentials')
        try:
            for credential in credentials_list:
                if os.environ[credential]:
                    pass
            return True
        except Exception:
            logger.error("Valid credentials not found for provider {}".format(self._provider))
            return False

    def call_provider(self, common_name) -> str:
        """Generate certbot commands based on provider name"""
        pass

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

from .dns_engine import DnsEngine
import os
import subprocess
from ..backend import VaultStoreEngine


class DnsProviderAWS(DnsEngine):
    def __init__(self, provider) -> None:
        """Constructor for DnsProviderAWS"""
        super().__init__()

    def call_provider(self, common_name) -> str:
        """Return provider specific certbot commands"""
        if super().validate_provider_credentials():
            work_dir = "/certdata/var/lib/letsencrypt/"
            logs_dir = "/certdata/var/log/letsencrypt/"
            config_dir = "/certdata/etc/letsencrypt/"
            command = "certbot certonly --dns-route53 -d {} " \
               "--work-dir {} " \
               "--logs-dir {} " \
               "--config-dir {}".format(common_name, work_dir, logs_dir, config_dir)
            response = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if response.returncode == 0:
                logger.info("certificate for domain name {} generated successfully".format(common_name))
                logger.info("Writing certs to vault..")
                chain_file = "{}/live/{}/chain.pem".format(common_name, config_dir)
                cert_file = "{}/live/{}/cert.pem".format(common_name, config_dir)
                privkey_file = "{}/live/{}/privkey.pem".format(common_name, config_dir)
                return chain_file




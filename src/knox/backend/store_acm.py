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
"""

import sys
import json
import hvac
import boto3
from botocore.exceptions import ClientError, EndpointConnectionError
from dynaconf import settings
from datetime import datetime,time
from jinja2 import Template, Environment, FileSystemLoader
from loguru import logger

from .store_engine import StoreEngine
from .store_object import StoreObject
#from .store_vault import VaultStoreEngine
from .store_vault import VaultClient

class ACMStoreEngine(StoreEngine):
    """
    ACMStoreEngine Class
    CRUD operations for Aws Certificate Manager
    """

    __AwsErrors = (ClientError, EndpointConnectionError)

    def __call__(self):
        pass

    def __init__(self, profile_name=None, region=None):
        self.profile_name = profile_name if profile_name is not None else settings.AWS_PROFILE
        self.region = region if region is not None else settings.AWS_REGION
        self.CertArn = None
        self.__path = None
        #self.__vault_url = settings.VAULT_URL
        #self.__vault_token = settings.VAULT_TOKEN
        #self.__approle = settings.VAULT_APPROLE
        #self.__secretid = settings.VAULT_SECRET_ID
        self.__vault_mount = settings.VAULT_MOUNT
        #self.__vault_client = hvac.Client(url=self.__vault_url, token=self.__vault_token)
        self.__vault_client = hvac.Client(url=self.__vault_url)
        self.__session = boto3.Session(profile_name=self.profile_name,region_name=self.region)

    def read(self):
        """ ACM Store Engine Read the certificate to specified region and account """

        try:
            acm_res = self.__session.client('acm').list_certificates(
                CertificateStatuses=['ISSUED'],
                MaxItems=123
            )
            certs = acm_res.get('CertificateSummaryList')

        except self.__AwsErrors as e:
            logger.error(f'[ACMStoreEngine]: Exception listing certificates from ACM {e}')
            exit(1)

        return certs

    def write(self, obj: StoreObject):
        """ ACM Store Engine Write the certificate to specified region and account

            :param obj: The StoreObject to persist in AWS ACM Store
            :type obj: StoreObject
            :return: bool

        """

        try:
            cert = obj.data['cert_body'].get('public')
            key = obj.data['cert_body'].get('private')
            chain = obj.data['cert_body'].get('chain')
            self.__path = obj.path_name
        except Exception as e:
            logger.error(f'[ACMStoreEngine]: cert error {e}')

        logger.debug(f'[ACMStoreEngine]:\nPUB:\n{cert}\nKEY:\n{key}\nCHAIN:\n{chain}\n')

        try:
            acm_res = self.__session.client('acm').import_certificate(
                Certificate = cert,
                PrivateKey = key,
                Tags = [
                    {'Key': 'Name','Value': 'App or Service Name'},
                    {'Key': 'Environment','Value': 'Development'},
                    {'Key': 'Team','Value': 'RESTeam'},
                    {'Key': 'contact','Value': 'robert@vault.knox'}
                ]
            )
            self.CertArn = acm_res.get('CertificateArn')
            self.__delivery_info()
            logger.info(f'[ACMStoreEngine]: Certificate uploaded:\nRegion: {self.region}\nAccount: {self.profile_name}\nCertARN: {self.CertArn}')
            return True

        except self.__AwsErrors as e:
            logger.error(f'[ACMStoreEngine]: Exception listing certificates from ACM {e}')
            sys.exit(1)

    # Private method
    def __delivery_info(self):
        """ ACM Store delivery information """
        time_utc_now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        tmpl = Environment(loader=FileSystemLoader('templates'))
        tmpl_delivery = tmpl.get_template('delivery_template.js')
        output = tmpl_delivery.render(time_utc_now=time_utc_now,region=self.region,profile=self.profile_name,certarn=self.CertArn)

        #a = VaultClient.connect()
        #print(a)
        client = self.__vault_client
        mp = self.__vault_mount
        full_path = f'{self.__path}/delivery_info'

        try:
            client.secrets.kv.v2.create_or_update_secret(path=full_path, mount_point=mp, secret=json.loads(output))

        except Exception as e:
            logger.error(f'[ACMStoreEngine]: Failed to write delivery_info to Vault {e}')

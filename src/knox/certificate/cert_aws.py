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
import boto3
from botocore.exceptions import ClientError, EndpointConnectionError
from dynaconf import settings
from datetime import datetime,time
from jinja2 import Template, Environment, FileSystemLoader
from loguru import logger
from ..backend import StoreObject

class AWSCert:
    """
    AWSCert Class
    CRUD operations for Aws Certificate Manager
    """

    __AwsErrors = (ClientError, EndpointConnectionError)

    def __call__(self):
        pass

    def __init__(self,profile_name=None, region=None):
        self.profile_name = profile_name if profile_name is not None else settings.AWS_PROFILE
        self.region = region if region is not None else settings.AWS_REGION
        self.__session = boto3.Session(profile_name=self.profile_name,region_name=self.region)
        self.pub_cert = None
        self.CertArn = None

    def list_cert(self):
        try:
            acm_res = self.__session.client('acm').list_certificates(
                CertificateStatuses=['ISSUED'],
                MaxItems=123
            )
            certs = acm_res.get('CertificateSummaryList')
        except self.__AwsErrors as e:
            logger.error(f'[AWSCert]: Exception listing certificates from ACM {e}')
            sys.exit(1)
        return certs

    def get_cert(self,cert_arn=None):
        self.cert_arn = cert_arn if cert_arn is not None else None
        try:
            acm_res = self.__session.client('acm').get_certificate(
                CertificateArn=self.cert_arn,
            )
            pub_cert = acm_res.get('Certificate')
            self.delivery_info()
            #print(pub_cert)
        except self.__AwsErrors as e:
            logger.error(f'[AWSCert]: Exception listing certificates from ACM {e}')
            sys.exit(1)
        return self.pub_cert

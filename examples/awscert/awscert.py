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

from datetime import datetime

import boto3
from botocore.exceptions import ClientError
from dynaconf import settings
from jinja2 import Environment
from jinja2 import FileSystemLoader


class AwsCert:
    """
    AwsCert Class
    CRUD operations for Aws Certificate Manager
    """

    def __call__(self):
        pass

    def __init__(self, profile_name=None, region=None):
        self.profile_name = profile_name if profile_name is not None else settings.AWS_PROFILE
        self.region = region if region is not None else settings.AWS_REGION
        self.pub_cert = None
        self.CertArn = None

    def list_cert(self):
        _session = boto3.Session(profile_name=self.profile_name, region_name=self.region)
        try:
            acm_res = _session.client('acm').list_certificates(
                CertificateStatuses=['ISSUED'],
                MaxItems=123
            )
            certs = acm_res.get('CertificateSummaryList')
        except ClientError as e:
            print(e)
            exit(1)
        return certs

    def get_cert(self, cert_arn=None):
        self.cert_arn = cert_arn if cert_arn is not None else None
        _session = boto3.Session(profile_name=self.profile_name, region_name=self.region)
        try:
            acm_res = _session.client('acm').get_certificate(
                CertificateArn=self.cert_arn,
            )
            self.pub_cert = acm_res.get('Certificate')
            self.delivery_info()
        # print(pub_cert)
        except ClientError as e:
            print(e)
            exit(1)
        return self.pub_cert

    # def put_cert(self,cert_arn=None,cert=None,prv_key=None,cert_chain=None):
    def upload_cert(self, cert_arn=None, cert=None, prv_key=None, cert_chain=None):
        print(f'\nProfile: {self.profile_name}\tRegion: {self.region}\n')
        _session = boto3.Session(profile_name=self.profile_name, region_name=self.region)
        try:
            acm_res = _session.client('acm').import_certificate(
                Certificate=cert,
                PrivateKey=prv_key,
                Tags=[
                    {'Key': 'Name', 'Value': 'Project or App name'},
                    {'Key': 'Environment', 'Value': 'Testing'},
                    {'Key': 'Team', 'Value': 'RES Team'},
                    {'Key': 'contact', 'Value': 'Robert'}
                ]
            )
            self.CertArn = acm_res.get('CertificateArn')
            self.delivery_info()
        # print(acm_res)
        except ClientError as e:
            print(e)
            exit(1)

    def delivery_info(self):
        time_utc_now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        tmpl = Environment(loader=FileSystemLoader('templates'))
        tmpl_delivery = tmpl.get_template('delivery_template.js')
        output = tmpl_delivery.render(time_utc_now=time_utc_now, region=self.region, profile=self.profile_name,
                                      certarn=self.CertArn)
        with open('out_delivery_info.json', 'w+') as f:
            f.write(output)

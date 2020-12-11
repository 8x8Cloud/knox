import pytest
import time
import os
import requests
import json
import click
from click.testing import CliRunner
from tests.src.knox.knox import Knox

headers = {'Content-Type': 'application/json','X-Vault-Token': 'knox'}

def admin_user_read_policiescreation(vault_container,shared_datadir):
    for filename in os.listdir(shared_datadir):
        if filename.startswith('cert_'):
           (policyname, ext) = os.path.splitext(filename)
           contents = (shared_datadir / filename).read_text()
           vault_container.sys.create_or_update_policy(
              name=policyname[5:],
              policy=contents,
           )
        else:
           pass

def test_admin_user_read_policiescreation(vault_container,shared_datadir):
    admin_user_read_policiescreation(vault_container,shared_datadir)
    policies = vault_container.sys.list_policies()['data']['policies']
    assert 'admin-policy' in policies
    assert 'read-policy' in policies
    assert 'user-policy' in policies


def approle_roleid_secretid_creation(vault_container,shared_datadir):
    vault_container.sys.enable_auth_method(
       method_type='approle',
    )
    vault_container.sys.enable_secrets_engine(
       backend_type='kv',
       path='certificate',
    )

    approleid = ''
    approlesecret = ''

    for filename in os.listdir(shared_datadir):
         if filename.startswith('approle'):
            contents = (shared_datadir / 'approle-role-certificatestore.json').read_text()
            requests.post(url="http://127.0.0.1:8200/v1/auth/approle/role/certificatestore", headers=headers, data=contents)
            response = requests.get(url="http://127.0.0.1:8200/v1/auth/approle/role/certificatestore/role-id", headers=headers)
            approleid = json.loads(response.content.decode('utf-8'))['data']['role_id']
            print(approleid)
            contents = (shared_datadir / 'approle-secret.json').read_text()
            requests.post(url="http://127.0.0.1:8200/v1/auth/approle/role/certificatestore/custom-secret-id", headers=headers, data=contents)
            approlesecret = json.loads(contents)['secret_id']
            print(approlesecret)
         else:
            pass

    vault_container.auth_approle(approleid, approlesecret)

def test_approle_roleid_secretid_creation(vault_container,shared_datadir):
    approle_roleid_secretid_creation(vault_container,shared_datadir)
    ctx = click.Context
    ctx.obj = dict()
    ctx.obj['STORE_FIND_NAME'] = "www.learning.com"
    ctx.obj['STORE_FIND_OUTPUT'] = "JSON"
    ctx.obj['LOG_LEVEL'] = "INFO"
    knox = Knox(ctx)
    results = knox.store.find(pattern=name)  # noqa F841
    #return ctx

    #runner.invoke(cli, ['cert', '--pub', '/root/pytest-learning/knox/tests/policy_creation/client-pub.pem', '--key', '/root/pytest-learning/knox/tests/policy_creation/client-key.pem', 'save', 'hello' ])

import pytest
import requests
import hvac
import os
import time
import json
from requests.exceptions import ConnectionError

headers = {'Content-Type': 'application/json', 'X-Vault-Token': 'knox'}


def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope="session")
def vault_container(docker_ip, docker_services):

    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("vault", 8200)
    vaulturl = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(vaulturl)
    )

    client = hvac.Client(
                url=vaulturl,
                token='knox'
                )

    return client


@pytest.fixture(scope="function")
def vault_initialized(vault_container, docker_ip, shared_datadir):
    for filename in os.listdir(shared_datadir):
        if filename.startswith('cert_'):
            (policyname, ext) = os.path.splitext(filename)
            print(f"loading {policyname}")
            contents = (shared_datadir / filename).read_text()
            vault_container.sys.create_or_update_policy(
                name=policyname[5:],
                policy=contents,
            )

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
            requests.post(url="http://127.0.0.1:8200/v1/auth/approle/role/certificatestore", headers=headers,
                          data=contents)
            response = requests.get(url="http://127.0.0.1:8200/v1/auth/approle/role/certificatestore/role-id",
                                    headers=headers)
            approleid = json.loads(response.content.decode('utf-8'))['data']['role_id']
            print(f"app role id: {approleid}")
            contents = (shared_datadir / 'approle-secret.json').read_text()
            requests.post(url="http://127.0.0.1:8200/v1/auth/approle/role/certificatestore/custom-secret-id",
                          headers=headers, data=contents)
            approlesecret = json.loads(contents)['secret_id']
            print(f"app role secret: {approlesecret}")
        else:
            pass

    vault_container.auth_approle(approleid, approlesecret)

    client = hvac.Client(
                url=f"http://{docker_ip}:8200",
                token='knox'
                )

    return client

import pytest
import requests
import hvac
import os
import time
import json
from requests.exceptions import ConnectionError

headers = {'Content-Type': 'application/json', 'X-Vault-Token': 'knox'}


class KnoxTestFixtureData:
    """Test setup object"""

    def __init__(self):
        """Constructor for KnoxTextFixtures"""


knoxtestfixturedata = KnoxTestFixtureData


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
    vaulturl = f"http://{docker_ip}:{port}"
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

    # Apply Vault policies
    for filename in os.listdir(shared_datadir):
        if filename.startswith('cert_'):
            (policyname, ext) = os.path.splitext(filename)
            contents = (shared_datadir / filename).read_text()
            vault_container.sys.create_or_update_policy(
                name=policyname[5:],
                policy=contents,
            )

    # Enable Vault AppRole Auth Method
    vault_container.sys.enable_auth_method(
       method_type='approle',
    )

    # Enable Secrets engine
    vault_container.sys.enable_secrets_engine(
       backend_type='kv',
       path='certificate',
    )

    approleid = ''
    approlesecret = ''

    # Create Approle entity and associated secret
    for filename in os.listdir(shared_datadir):
        if filename.startswith('approle'):
            contents = (shared_datadir / 'approle-role-certificatestore.json').read_text()
            requests.post(url=f"http://{docker_ip}:8200/v1/auth/approle/role/certificatestore", headers=headers,
                          data=contents)
            response = requests.get(url=f"http://{docker_ip}:8200/v1/auth/approle/role/certificatestore/role-id",
                                    headers=headers)
            approleid = json.loads(response.content.decode('utf-8'))['data']['role_id']
            print(f"app role id: {approleid}")
            knoxtestfixturedata.approleid = approleid
            contents = (shared_datadir / 'approle-secret.json').read_text()
            requests.post(url=f"http://{docker_ip}:8200/v1/auth/approle/role/certificatestore/custom-secret-id",
                          headers=headers, data=contents)
            approlesecret = json.loads(contents)['secret_id']
            print(f"app role secret: {approlesecret}")
            knoxtestfixturedata.approlesecret = approlesecret
        else:
            pass

    vault_container.auth_approle(approleid, approlesecret)

    client = hvac.Client(
                url=f"http://{docker_ip}:8200",
                token='knox'
                )

    return client

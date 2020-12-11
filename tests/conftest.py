import pytest
import requests
import os
import hvac
from requests.exceptions import ConnectionError
import time
from dynaconf import settings


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

    #print(client.is_authenticated())

    return client

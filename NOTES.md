
Local Development Setup

```shell script
# development only!
docker stop dev-vault
docker rm dev-vault
docker run \
--cap-add=IPC_LOCK \
-p 8201:8201 \
-p 8200:8200 \
-e 'VAULT_DEV_ROOT_TOKEN_ID=knox' \
-d --name=dev-vault \
vault

```

Running Knox container

```shell script
docker run -it --net=host -v /Users/ljohnson/dev/git.8x8.com/auto/hashicorp/vault/knox/examples/:/examples 8x8cloud/knox:vlocal sh



docker run --net=host \
-v /Users/ljohnson/dev/git.8x8.com/auto/hashicorp/vault/knox/examples/:/examples \
8x8cloud/knox:vlocal cert --save --pub /examples/sample_cert1.pem www.example.com


```

Pypi Publishing

```
# configure your ~/.pypirc with account details

# build with no errors or warnings
tox

# generate the artifacts to publish
python3 setup.py sdist bdist_wheel

# validate them
twine check dist/*.whl dist/*.gz

#publish them
twine upload --verbose dist/*.whl dist/*.gz
```

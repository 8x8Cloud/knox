

Local Development Setup

```shell script


docker run \
--cap-add=IPC_LOCK \
-p 8201:8201 \
-p 8200:8200 \
-e 'VAULT_DEV_ROOT_TOKEN_ID=knox' \
-d --name=dev-vault \
vault

```

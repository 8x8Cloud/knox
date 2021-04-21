# Permissions for uploading and reading the certificate body and metadata
# This should match the setting KNOX_VAULT_MOUNT
path "certificate/*"
{ capabilities = ["create", "read"] }

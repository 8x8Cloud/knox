# Permissions for administering the certificate body and metadata
# This should match the setting KNOX_VAULT_MOUNT
path "certificate/*"
{ capabilities = ["create", "read", "update", "delete", "list", "sudo"] }

# Permissions to allow knox to create certificate specific access policies
path "sys/policy/*"
{ capabilities = [ "update" ] }

path "sys/policy"
{ capabilities = [ "read" ] }

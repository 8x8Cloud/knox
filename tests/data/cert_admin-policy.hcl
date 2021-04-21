# Permissions for administering the certificate body and metadata
# This should match the setting KNOX_VAULT_MOUNT
path "certificate/*"
{ capabilities = ["create", "read", "update", "delete", "list", "sudo"] }

# Permissions to allow knox to create certificate specific access policies
path "sys/policy/*"
{ capabilities = [ "update" ] }

path "sys/policy"
{ capabilities = [ "read" ] }

# Allow knox to seed the kv store if it doesn't exist
# This requires using --admin hidden cli param
path "sys/mounts"
{ capabilities = [ "read","list" ]}

# This should match the setting KNOX_VAULT_MOUNT
path "sys/mounts/certificate"
{ capabilities = [ "create","update" ]}

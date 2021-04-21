# Read only permissions for just certificate metadata
# This should match the setting KNOX_VAULT_MOUNT
path "certificate/" { capabilities = ["list"] }
path "certificate/+/" { capabilities = ["list"] }
path "certificate/+/cert_info" { capabilities = ["read"] }
path "certificate/+/+/" { capabilities = ["list"] }
path "certificate/+/+/cert_info" { capabilities = ["read"] }
path "certificate/+/+/+/" { capabilities = ["list"] }
path "certificate/+/+/+/cert_info" { capabilities = ["read"] }
path "certificate/+/+/+/+/" { capabilities = ["list"] }
path "certificate/+/+/+/+/cert_info" { capabilities = ["read"] }
path "certificate/+/+/+/+/+/" { capabilities = ["list"] }
path "certificate/+/+/+/+/+/cert_info" { capabilities = ["read"] }
path "certificate/+/+/+/+/+/+/" { capabilities = ["list"] }
path "certificate/+/+/+/+/+/+/cert_info" { capabilities = ["read"] }
path "certificate/+/+/+/+/+/+/+/" { capabilities = ["list"] }
path "certificate/+/+/+/+/+/+/+/cert_info" { capabilities = ["read"] }

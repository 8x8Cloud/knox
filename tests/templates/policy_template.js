path "{{cert.policy_mount}}{{cert.path}}/{{cert.valid_name(cert.name)}}/{{cert.type}}/cert_body" {
  capabilities = [ "read" ]
}
path "{{cert.policy_mount}}{{cert.path}}/{{cert.valid_name(cert.name)}}/{{cert.type}}/cert_info" {
  capabilities = [ "read" ]
}

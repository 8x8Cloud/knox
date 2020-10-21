path "{{cert.mount}}/data{{cert.path}}/{{cert.valid_name(cert.name)}}/{{cert.type}}/cert_body" {
  capabilities = [ "read" ]
}
path "{{cert.mount}}/data{{cert.path}}/{{cert.valid_name(cert.name)}}/{{cert.type}}/cert_info" {
  capabilities = [ "read" ]
}

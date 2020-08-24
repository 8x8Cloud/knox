#!/bin/sh

knox store find *.com | jq '.[] | select(.days_to_expire <= 30)' | jq -r '.common_name' | xargs -I {} certbot certonly -n --agree-tos --dns-route53 -d {} --email <EMAIL> --server https://acme-v02.api.letsencrypt.org/directory --deploy-hook "knox cert --pub /etc/letsencrypt/live/{}/cert.pem --chain /etc/letsencrypt/live/{}/chain.pem --key /etc/letsencrypt/live/{}/privkey.pem save {}"

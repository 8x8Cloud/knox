#!/bin/sh

#------------------------------------------------------------------------------------------
# Author: Kadiri Purushotham Reddy
# version: 1.0.0
# Description: Entrypoint script that renews the certificate based on the dns service type
#-------------------------------------------------------------------------------------------

set -e

IFS=$'\n'

case $DNSPLUGIN in
     "dns-route53")
          letsencryptexpirycerts=`knox store find $DOMAINSEARCH |  jq  ".[] | select(.issuer==\"Let's Encrypt\" and .days_to_expire <= 30 and .issuer != null)"`
          if [ -z "${letsencryptexpirycerts}" ]
          then
                echo "There are no LetsEncrypt certificates due for renewal."
          else
                knox store find $DOMAINSEARCH | jq  ".[] | select(.issuer==\"Let's Encrypt\" and .days_to_expire <= 30 and .issuer != null)" | jq -r '.common_name' | xargs -I {} certbot certonly -n --agree-tos --$DNSPLUGIN --force-renewal -d {} --email $EMAIL --deploy-hook "knox cert --pub /etc/letsencrypt/live/{}/cert.pem --chain /etc/letsencrypt/live/{}/chain.pem --key /etc/letsencrypt/live/{}/privkey.pem save {}"
          fi
          ;;
     "cloudflare")
          echo "issuer is : FreeCertificate Inc"
          break
          ;;
     *)
          echo "Sorry, I don't understand"
          ;;
esac

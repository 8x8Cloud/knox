
## Local Development Setup

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

## Running Knox container

```shell script
docker run -it --net=host -v /Users/ljohnson/dev/git.8x8.com/auto/hashicorp/vault/knox/examples/:/examples 8x8cloud/knox:vlocal sh



docker run --net=host \
-v /Users/ljohnson/dev/git.8x8.com/auto/hashicorp/vault/knox/examples/:/examples \
8x8cloud/knox:vlocal cert --save --pub /examples/sample_cert1.pem www.example.com


```


## Certbot

ideas:

* instead of python code to call certbot, call knox from certbot --deploy-hook to store renewed certificate
* k8s deployment with pvc of certbot configured from configmap 

```
# https://certbot.eff.org/docs/install.html#running-with-docker
# https://hub.docker.com/r/certbot/dns-route53
# https://github.com/certbot-docker/certbot-docker
# https://certbot.eff.org/docs/using.html#certbot-commands

  --deploy-hook DEPLOY_HOOK
                        Command to be run in a shell once for each
                        successfully issued certificate. For this command, the
                        shell variable $RENEWED_LINEAGE will point to the
                        config live subdirectory (for example,
                        "/etc/letsencrypt/live/example.com") containing the
                        new certificates and keys; the shell variable
                        $RENEWED_DOMAINS will contain a space-delimited list
                        of renewed certificate domains (for example,
                        "example.com www.example.com" (default: None)


# non-interactive with deploy-hook
# probably need to have one of these for every DNS Authoritative Server
#
mkdir -p /Users/ljohnson/dev/le/etc/letsencrypt
mkdir -p /Users/ljohnson/dev/le/var/lib/letsencrypt
mkdir -p /Users/ljohnson/dev/le/var/log/letsencrypt

docker run --net=host   \
            -v "/Users/ljohnson/dev/le/etc/letsencrypt:/etc/letsencrypt" \
            -v "/Users/ljohnson/dev/le/var/lib/letsencrypt:/var/lib/letsencrypt" \
            -v "/Users/ljohnson/dev/le/var/log/letsencrypt:/var/log/letsencrypt" \
            --rm --name certbot \
            certbot/dns-route53 certonly \
            		--dry-run \
            		--noninteractive \
            		--dns-route53 \
            		--agree-tos \
            		--register-unsafely-without-email \
            		--deploy-hook "echo 'knox cert store'" \
            		-d www.example.com \
            		-d web.anotherexample.com
        
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator dns-route53, Installer None
Obtaining a new certificate
Performing the following challenges:
dns-01 challenge for web.anotherexample.com
dns-01 challenge for www.example.com
Cleaning up challenges
IMPORTANT NOTES:
 - Your account credentials have been saved in your Certbot
   configuration directory at /etc/letsencrypt. You should make a
   secure backup of this folder now. This configuration directory will
   also contain certificates and private keys obtained by Certbot so
   making regular backups of this folder is ideal.
Unable to locate credentials
To use certbot-dns-route53, configure credentials as described at 
https://boto3.readthedocs.io/en/latest/guide/configuration.html#best-practices-for-configuring-credentials 
add the necessary permissions for Route53 access.

```

## Certificate Transparency Project

```
# Get all certs associated with a domain as json
https://crt.sh/?Identity=8x8.com&output=json

# Using its ID grab the SHA-256 ID/string
https://crt.sh/?id=2865351373

# Use the SHA-256 ID/string to get the public pem
https://censys.io/certificates/cb99c1a7da13016397180d8aa7afac3088626aba10391113536ddb568274e215/pem/raw

# Store it using knox

# Add links to crt and censys.io to Knox Cert metadata

```








## Travis CI Command Line

```
>brew install ruby
>gem install travis

>travis login \
  --org \
  --github-token <REDACTED>
>Successfully logged in as rljohnsn!
 

>travis repos --active
8x8Cloud/knox (active: yes, admin: yes, push: yes, pull: yes)
Description: Certificate managment utilities using a Vault backend

8x8Cloud/swagger2raml (active: yes, admin: yes, push: yes, pull: yes)
Description: A utility to generate RAML documentation from Swagger JSON

>travis token
Your access token is <REDACTED>


>travis encrypt --org \
	--token <REDACTED> \
	--repo 8x8Cloud/knox \
	--debug --debug-http \
	<STRING TO ENCRYPT>
	--add deploy.password

```

## Travis CI PyPi Publishing, added to .travis.yml

```
deploy:
  provider: pypi
  user: __token__
  skip_existing: true
  password:
    secure: <ENCRYPTED REDACTED>
  on:
    tags: true
    branch: develop
```


## Pypi Publishing

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













# Banners


## [Text Image](https://www.text-image.com/convert/pic2ascii.cgi)

```

```       ``      ``       ```
``` ````  `  ```` ``  ```` ```
``` ````     ````     ```` ```
```  ````````````````````  ```
`````  ````````````````  `````
`````  ```````  ```````  `````
`````  `````  ``  `````` `````
````  `````` ```` ``````  ````
````  `````` ```` ``````  ````
````  ```            ```  ````
```  ```` ```` ````` ````  ```
`  `````` ```` ````` ``````  `
`  `````` `````````` ``````  `
` ```````  ````````` ``````` `

```

## [ASCII Art Generator](https://www.ascii-art-generator.org/)

```

MMMk'..........:KWd............dWK:..........,OMMM
MMMx. .;cccc'  ,KWo  .:cccc:.  oWK,  'cccc;. .kMMM
MMMx. 'OMMMWx. 'xO:  :XMMMMNc  :0x'  oWMMM0' .kMMM
MMWx. .OMMMWd.   .   :XMMMMNc   .    oWMMM0' .kMMM
MMMx. .OMMMMKolllllllkNMMMMWOollllllo0WMMM0' .kMMM
MMMO'  'oKWMMMMMMMMMMMMMMMMMMMMMMMMMMMMWXd,  ,0MMM
MMMW0o'  .c0WMMMMMMMMMMMMMMMMMMMMMMMMMKl.  ,dKWMMM
MMMMMWXo.  oWMMMMMMMMMMMMMMMMMMMMMMMMWx. .dNMMMMMM
MMMMMMMk. .kMMMMMMMMWXOxddxOXWMMMMMMMMO' .OMMMMMMM
MMMMMMWo  ;KMMMMMMMKl.      'lKMMMMMMMX:  dWMMMMMM
MMMMMMX;  lNMMMMMMX:  ,oxdl'  ;KMMMMMMWo  :XMMMMMM
MMMMMMO. .xMMMMMMMk. 'OMMMWx. .kMMMMMMMk. '0MMMMMM
MMMMMWd. '0MMMMMMMk. ,0MMMMk. .xMMMMMMMK; .xWMMMMM
MMMMMNc  cNMMMMMMMk. ,0MMMMk. .xMMMMMMMNl  cNMMMMM
MMMMM0, .dWMMMNXXXd. 'kXXXXx. .oXXXNWMMMx. ,KMMMMM
MMMMMk. 'OMMMWd..'.   ......   .''.;OMMM0' .kMMMMM
MWWWXl  ;XMMMNc ,kd;'''...'''',oOo..kMMMN:  lNNWWM
M0:,'.  oWMMMNc cNWWNNk,.'lKNNNWMO..kMMMWd. .',cKM
Wo  .',c0MMMMNc cNMMMWO,.,oNMMMMMO..kMMMM0:''. .dW
X:  cXWWMMMMMNc cNMMMMWxo0NMMMMMMO..kMMMMWWNXl  cN
O. .xWMMMMMMMNc cNMMMMMXXNWMMMMMMO..kMMMMMMMMk. '0
d. '0MMMMMMMMNc :KNNNNNNNNNNNNNNNk..kMMMMMMMMK, .x
:  ;OKKKKKKKK0; ..'''''''''''''''. .oKKKKKKKK0:  c
.   ..........                       .........   '
,................................................;

```



```

MMO,........lNk..........kNl........,0MM
MMO. ;xkko. cXx. ckkkkc..xXc .lkkk; .OMM
MMO. lWMM0' .,. .xWMMMk. .,. 'OMMWo 'OMM
MMO. cNMMXxcccccoKMMMMKoclcccdXMMNl 'OMM
MMK:..;xXWMMMMMMMMMMMMMMMMMMMMWNk:..cXMM
MMMNk:. ;KMMMMMMMMMMMMMMMMMMMMXc .cONMMM
MMMMMK; ,KMMMMMMWNK00KNWMMMMMMX; ;XMMMMM
MMMMMO. cNMMMMWKl'....'lKWMMMMWl '0MMMMM
MMMMWd..xWMMMMX; 'dkko. ;KMMMMMk..xWMMMM
MMMMNc '0MMMMMO' oWMMNc .OMMMMMK, cNMMMM
MMMM0' :XMMMMMO' oWMMNc .OMMMMMNc ,KMMMM
MMMMx. dWMWNXXx. cKKK0: .dKKXWMWd..kMMMM
MMMWl .OMMWo',,   ....   ,;';0MMO' lNMMM
W0xo' ;XMMNc.dKxol,.':ooxK0;.OMMX: 'oxKW
X;  ..dWMMNc.kMMMX:.,xWMMMX;.OMMWd..  :X
O. :0XNMMMNc.kMMMWkd0XMMMMX;.OMMMNX0c '0
o .xWMMMMMNc.kMMMMNNWWMMMMX;.OMMMMMMk..d
: '0MWWWWWNc.:dddddddddddxo..OWWWWWM0, :
. .,::::::;.                 '::::::;. '
'......................................'


```


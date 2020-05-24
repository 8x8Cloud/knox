
Local Development Setup

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

Running Knox container

```shell script
docker run -it --net=host -v /Users/ljohnson/dev/git.8x8.com/auto/hashicorp/vault/knox/examples/:/examples 8x8cloud/knox:vlocal sh



docker run --net=host \
-v /Users/ljohnson/dev/git.8x8.com/auto/hashicorp/vault/knox/examples/:/examples \
8x8cloud/knox:vlocal cert --save --pub /examples/sample_cert1.pem www.example.com


```

Travis CI Command Line

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

Travis CI PyPi Publishing, added to .travis.yml

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


Pypi Publishing

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


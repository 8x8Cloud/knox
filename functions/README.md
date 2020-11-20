# Openfaas serverless framework for kubernetes

- [Openfaas](#openfaas)
   - [Overview](#overview)
   - [Supported Environments](#supported-environments)
   - [Supported Languages](#supported-languages)
   - [Installation](#installation)
	- [Pre-requisites](#pre-requisites)
	- [Installing openfaas using arkade utility (Recommended)](#installing-openfaas-using-arkade-utility-recommended)
	- [Installing openfaas using helm](#installing-openfaas-using-helm)
	- [Examples](#examples)
	    - [First Python function](#first-python-function)
	    - [Fetching expiry certs from vault and displaying them on web ui](#fetching-expiry-certs-from-vault-and-displaying-them-on-web-ui)

### Overview

**`OpenFaaS`** makes it easy for developers to deploy event-driven functions and microservices to Kubernetes without repetitive, boiler-plate coding. Package your code or an existing binary in a Docker image to get a highly scalable endpoint with auto-scaling and metrics. Following are some of the features of openfaas.

- Ease of use through UI portal and one-click install
- Write functions in any language for Linux or Windows and package in Docker/OCI image format
- Portable - runs on existing hardware or public/private cloud with Kubernetes or containerd
- CLI available with YAML format for templating and defining functions
- Auto-scales as demand increases

**Openfaas components**

**Prometheus** - metrics and time-series  
**Linkerd** - service mesh  
**OpenFaaS** - management and auto-scaling of compute - PaaS/FaaS  
**NATS** - asynchronous message bus / queue  
**Kubernetes** - declarative, extensible, scale-out, self-healing clustering  

### Supported Environments

- openshift
- kubernetes
   - **`Local clusters`**
      - k3d
	  - kinD(kubernetes in docker)
	  - k3s -  a light-weight Kubernetes distribution ideal for edge and development - compatible with Raspberry Pi & ARM64 (Equinix Metal, AWS Graviton, etc)
	  - minikube
	  - microk8s
   - **`Public cloud`**
     - GKE(Google Kubernetes Engine)
	 - Amazon EKS
	 - Azure AKS
	 - Digital Ocean kubernetes
- docker swarm

### Supported Languages

- csharp
- dockerfile
- go
- java11
- node
- php
- python
- ruby

### Installation

Openfaas can be installed on any of the supported environments. We are going to  install on the k3d cluster(local k8s environment).

### Pre-requisites

- **docker** - Refer to [docker docs](https://docs.docker.com/get-docker/) for installation steps. Also makesure docker service is up and running.
- **kubectl** - Following command is for linux operating systems. For other operating systems refer to [docs](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
```
 curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
 chmod +x kubectl
 mv kubectl /usr/bin/
 ```
- **k3d** 

     Run the following command to install k3d. For more details to refer [k3d docs](https://k3d.io/)

	```
	wget -q -O - https://raw.githubusercontent.com/rancher/k3d/main/install.sh | bash
	```
	To verify the installed k3d version run the following command.

	```
	k3d --version
	```

	Lets create a kubernetes cluster with 1 master & 2 workers using k3d utility.
	
    **syntax**:  k3d cluster create `<cluster-name`> \-\-agents 2
	
	for example:
	```
	k3d cluster create dev --agents 2
	```
    
	Run the following command to makesure cluster is created correctly.
	
	```
	kubectl get nodes
	```
	
	The above command should provide you an output with 1 master & 2 worker nodes.
- **faas-cli**

  This is a CLI for use with OpenFaaS - a serverless functions framework for Docker & Kubernetes.
  
  The CLI can be used to build and deploy functions to OpenFaaS. You can build OpenFaaS functions from a set of supported language templates (such as Node.js, Python, CSharp and Ruby). That means you just write a handler file such as (handler.py/handler.js) and the CLI does the rest to create a Docker image.
  
  faas-cli can be installed using the below command.
 
  ```
  # Linux
  curl -sSL https://cli.openfaas.com | sudo sh
  # Via brew
  brew install faas-cli
  ```
  For more details about faas-cli refer to [docs](https://github.com/openfaas/faas-cli)

### Installing openfaas using arkade utility (Recommended)

We have installed all the pre-requisites lets install openfaas using arkade utility. For more info on arkade refer to [docs](https://github.com/alexellis/arkade).

arkade can be installed using the below command.

```
curl -sLS https://dl.get-arkade.dev | sudo sh

arkade --help
ark --help  # a handy alias

```

Lets install openfaas using arkade. 

```
arkade install openfaas
        or		
arkade install openfaas --loadbalancer #On Public Cloud -> this creates a external loadbalancer from where openfaas gateway can be accessed
```

The above command create 2 new namespaces i.e `openfaas`(for openfaas components) & `openfaas-fn`(for functions).

All the `openfaas` components are deployed to `openfaas` namespace.
All the openfaas functions gets deployed to `openfaas-fn`. We have not deployed any functions yet. Hence there are no functions in this `openfass-fn` namespace.
To Access the openfaas gateway, we need to do expose service using either  port-forward, Nodeport, Loadbalancer. Run the following commands.

```
# Forward the gateway to your machine
kubectl rollout status -n openfaas deploy/gateway
kubectl port-forward --address 0.0.0.0 -n openfaas svc/gateway 8080:8080 &

# If basic auth is enabled, you can now log into your gateway:
PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
```

Now `openfaas gateway` can be accessed at \<node-ipaddress\>:8080. Browser prompts for credentials enter username as `admin`, password stored in the variable $PASSWORD.

As you can see in the gateway ui, there are no functions which is expected because we have not deployed any functions yet. 

Lets authenticate to openfaas gateway using faas-cli

```
PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
echo -n $PASSWORD | faas-cli login --username admin --password-stdin
```

### Installing openfaas using helm

Install the helm

```
arkade get helm
       or
curl -sSLf https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```
Lets create two namespaces, one for the OpenFaaS core services and one for the functions.

```
kubectl apply -f https://raw.githubusercontent.com/openfaas/faas-netes/master/namespaces.yml
```
You will now have openfaas and openfaas-fn. If you want to change the names or to install into multiple installations then edit namespaces.yml.

Add the OpenFaaS helm chart:
```
helm repo add openfaas https://openfaas.github.io/faas-netes/
```

Now decide how you want to expose the services and edit the helm upgrade command as required.

- To use NodePorts (default) pass no additional flags
- To use a LoadBalancer add --set serviceType=LoadBalancer
- To use an IngressController add --set ingress.enabled=true

> **Note:** even without a LoadBalancer or IngressController you can access your gateway at any time via kubectl port-forward as mentioned in previous section.

Now deploy OpenFaaS from the helm chart repo:

```
helm repo update \
 && helm upgrade openfaas --install openfaas/openfaas \
    --namespace openfaas  \
    --set functionNamespace=openfaas-fn \
    --set generateBasicAuth=true 
```

Retrieve the OpenFaaS credentials with:

```
PASSWORD=$(kubectl -n openfaas get secret basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode) && \
echo "OpenFaaS admin password: $PASSWORD"
```

**Generate basic-auth credentials**

The chart has a pre-install hook which can generate basic-auth credentials, enable it with --set generateBasicAuth=true.

Alternatively, you can set generateBasicAuth to false and generate or supply the basic-auth credentials yourself. This is the option you may want if you are using `helm template`.

```
# generate a random password	
PASSWORD=$(head -c 12 /dev/urandom | shasum| cut -d' ' -f1)
kubectl -n openfaas create secret generic basic-auth \
--from-literal=basic-auth-user=admin \
--from-literal=basic-auth-password="$PASSWORD"

echo "OpenFaaS admin password: $PASSWORD
```

To Access the openfaas gateway, we need to do expose service using either  port-forward, Nodeport, Loadbalancer. Run the following commands.

```
# Forward the gateway to your machine
kubectl rollout status -n openfaas deploy/gateway
kubectl port-forward --address 0.0.0.0 -n openfaas svc/gateway 8080:8080 &

# If basic auth is enabled, you can now log into your gateway:
PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
```

Now `openfaas gateway` can be accessed at \<node-ipaddress\>:8080. Browser prompts for credentials enter username as `admin`, password stored in the variable $PASSWORD. 

As you can see in the gateway ui, there are no functions which is expected because we have not deployed any functions yet. 

Lets authenticate to openfaas gateway using faas-cli

```
PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
echo -n $PASSWORD | faas-cli login --username admin --password-stdin
```

### Examples

As mentioned in supported languages section, functions can be developed in any programming language.

##### First Python function

create a new folder for our work.

```
mkdir -p functions
cd functions
```

The OpenFaaS CLI has a template engine built-in which can create new functions in a given programming language. The way this works is by reading a list of templates from the ./template location in your current working folder.

Before creating a new function make sure you pull in the official OpenFaaS language templates from GitHub via the [templates repository](#https://github.com/openfaas/templates).

```
faas-cli template pull
```

**Note**: Before you run the above command makesure faas-cli is authenticated to openfaas gateway(mentioned in previous sections).

let's scaffold a new Python function using the CLI.

```
faas-cli new --lang python3-debian hello-python
```

This creates three files for you:

> hello-python/handler.py  
> hello-python/requirements.txt  
> hello-python.yml  

Let's edit the handler.py file:

```
def handle(req):
    print("Hello! You said: " + req)
```

**handler.py**

All your functions should be specified in a YAML file like this - it tells the CLI what to build and deploy onto your OpenFaaS cluster.

Checkout the YAML file hello-python.yml

```
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  hello-python:
    lang: python
    handler: ./hello-python
    image: hello-python
```
**hello-python.yml**

- `gateway`- here we can specify a remote gateway if we need to, what the programming language is and where our handler is located within the filesystem.

- `functions` - this block defines the functions in our stack

- `lang`: python - even though Docker is used behind the scenes to package your function. You don't have to write your own Dockerfile unless you want to.

- `handler` - this is the folder / path to your handler.py file and any other source code you need

- `image` - this is the Docker image name. If you are going to push to the Docker Hub change the prefix from hello-python to include your Docker Hub account - i.e. \<dockerhub-username\>/hello-python

let\'s build the function.
```
faas-cli build -f ./hello-python.yml
```
You\'ll now see output from the Docker Engine as it builds your function into an image in your local Docker library. You'll see the image appear on docker images.


Lets upload the function to a remote registry*dockerhub by default).

```
faas-cli push -f ./hello-python.yml
```

Now the image has been pushed to dockerhub repo. but the image is private. Hence kubelet component is not authorized to pull the private images. Hence create a secret in openfaas-fn(namespace used for functions).

create secret using the below command.
```
kubectl create secret docker-registry my-private-repo \
    -n openfaas-fn \
    --docker-username=<dockerhub-username> \
    --docker-password=<dockerhub-password> \
    --docker-email=<dockerhub-email> \
    --docker-server=https://index.docker.io/v1/
```

Now edit the default service account configuration.

```
kubectl edit serviceaccount default -n openfaas-fn
```
At the bottom of the manifest add:

```
imagePullSecrets:
- name: my-private-repo
```

**Note:** If You want to push to a private registry(other than dockerhub) then update hello-python.yml as follows
```
version: 1.0
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080
functions:
  hello-python:
    lang: python3-debian
    handler: ./hello-python
    image: <registry>:<port>/repo
```


Lets Deploy the function.

```
faas-cli deploy -f ./hello-python.yml
```
Now the function is deployed and can be tested from both UI or using faas-cli.

**Using faas-cli:**

```
echo "Hello Kadiri" | faas-cli invoke hello-python
```

**UI:**

```
curl 127.0.0.1:8080/function/hello-python -d "It's Kadiri here"
```

**Note**: Refer to samples files - [hello-python.yml](functions/python-example/hello-python.yml) & [handler.py](functions/python-example/hello-python/handler.py).

### Fetching expiry certs from vault and displaying them on web ui

We will be fetching expiry certificates from vault and then displaying them on the webui.

we will using 2 functions.

- fetching-expirycerts -> fetches expiry certificates from vault   
- expirycerts-webui -> displaying expiry certificates on the Web UI    

**Note**:

The above functions are defined in [stack.yml](functions/expiry-certificates/stack.yml)
Replace the below values in [stack.yml](functions/expiry-certificates/stack.yml)

**\<openfaas-gateway\>**  
**\<docker-registry\>**  
**\<dockerhub-account\>**  
**\<vault url\>**  
**\<vault mountpoint\>**  
**\<vault engine\>**  
**\<vault token\>**  
**\<vault approle secretid\>**  
**\<vault approle\>**  


Replace the below values in [handler.py](functions/expiry-certificates/expirycerts-webui/handler.py)

**\<fetching-expirycerts function endpoint\>** -> for eg: http://34.80.205.5:8080/function/fetching-expirycerts.


Deploy the function.

```
cd functions/expiry-certificates
faas-cli up
```

After running the above command, navigate to below url to view the expiry certificates.

**\<openfaas-gateway\>/function/expirycerts-webui**

**Note**: Replace **\<openfaas-gateway\>** with your gateway.


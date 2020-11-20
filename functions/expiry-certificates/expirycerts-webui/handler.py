import requests
import os
import sys
from jinja2 import Environment,FileSystemLoader

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    r = requests.get(f"{os.getenv('OPENFAAS_HOST')}/function/fetching-expirycerts", data="store find \*")
    
    if r.status_code != 200:
       sys.exit("Error in fetching the expiry certs data, expected: %d, got: %d\n" % (200, r.status_code))

    env = Environment(loader=FileSystemLoader("/home/app/function/templates/"))
    template = env.get_template('data.html')
    return template.render(certs=r.json())

if __name__ == "__main__":
    main()

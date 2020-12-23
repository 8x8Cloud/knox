from random import randint
import requests
import os
import sys
import pandas as pd
from jinja2 import Environment,FileSystemLoader


_HEX = list('0123456789ABCDEF')

issuers = []

def randomcolor():
    return '#' + ''.join(_HEX[randint(0, len(_HEX)-1)] for _ in range(6))

def issuer_details(df):
    total = len(df['issuer'])
    for i in df['issuer'].unique():
        color = randomcolor()
        count = df[df['issuer'] == i]['issuer'].count()
        percentage = round(count*100/total,2)
        issuers_dict = {}
        issuers_dict['issuer'] = i
        issuers_dict['properties'] = [ color, count, percentage ] 
        issuers.append(issuers_dict)
        
def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    issuers.clear()

    r = requests.get(f"{os.getenv('OPENFAAS_HOST')}/function/fetching-expirycerts", data="store find \*")

    if r.status_code != 200:
       sys.exit("Error in fetching the expiry certs data, expected: %d, got: %d\n" % (200, r.status_code))

    env = Environment(loader=FileSystemLoader("/home/app/function/templates/"))
    template = env.get_template('data.html')
    df = pd.DataFrame(r.json())
    issuer_details(df)
    return template.render(certs=r.json(),issuers=issuers)

if __name__ == "__main__":
    main()

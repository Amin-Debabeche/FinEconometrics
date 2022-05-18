import sys
import requests
from FinEconometrics.scripts.twitter_fetching.functions.throttling import throttling

def connect_to_endpoint(url, headers, params, next_token = None):
    rate_url = "https://api.twitter.com/1.1/application/rate_limit_status.json"
    rate_params = {'resources' : 'help,users,search,statuses'}
    while True:
        status_response = requests.request("GET",rate_url, headers = headers, params = rate_params)
        if not status_response.ok:
            throttling(status_response)
            raise Exception(status_response.status_code, status_response.text)
        break
    params['next_token'] = next_token ##### ADD HERE CODE we do not need this except in the keyword url ?
    response = requests.request("GET", url, headers = headers, params = params)
    return response.json()

if __name__ == "__main__":
    url = sys.argv[1]
    headers = sys.argv[2]
    params = sys.argv[3]
    
    connect_to_endpoint(url, headers, params)
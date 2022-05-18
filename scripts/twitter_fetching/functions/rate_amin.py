import requests
from throttling_amin import throttling
from status_amin import status

def rate(headers):
    url = "https://api.twitter.com/1.1/application/rate_limit_status.json"
    params = {'resources' : 'help,users,search,statuses'}
    while True:
        status_response = requests.request("GET",url, headers = headers, params = params)
        status(status_response)
        remaining = int(status_response.headers["x-rate-limit-remaining"])
        if remaining <= 1:
            throttling(status_response)
            continue
        break
    return

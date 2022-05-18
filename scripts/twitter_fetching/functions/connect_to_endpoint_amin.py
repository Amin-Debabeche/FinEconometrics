import requests
import time
from rate_amin import rate
from status_amin import status

def connect_to_endpoint(url, headers, params):
    rate(headers)
    response = requests.request("GET", url, headers = headers, params = params)
    status(response)
    time.sleep(1)
    return response.json()

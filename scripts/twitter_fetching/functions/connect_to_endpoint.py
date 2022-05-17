import sys
import requests

def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

if __name__ == "__main__":
    url = sys.argv[1]
    headers = sys.argv[2]
    params = sys.argv[3]
    
    connect_to_endpoint(url, headers, params)
import pandas as pd
import connect_to_endpoint
import sys

def token(url, headers, params):
    while True:
        try:
            next_token = tweets_response['meta']['next_token']
        except:
            next_token = None
        if next_token is None:
            break
        tweets_response = connect_to_endpoint(url, headers, params, next_token)
        tmp = pd.json_normalize(tweets_response['data'])
    return tmp

if __name__ == "__main__":
    url = sys.argv[1]
    headers = sys.argv[2]
    params = sys.argv[3]
    
    token(url, headers, params)
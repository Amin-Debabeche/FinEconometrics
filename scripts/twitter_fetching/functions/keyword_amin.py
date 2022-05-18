import pandas as pd
from connect_to_endpoint_amin import connect_to_endpoint

def keyword_url(keywords, username, max_results, start_time, end_time_url, headers, id, token):
    """
    Search tweets based on keyword and username
    
    keyword: a string in form of 'xx OR xx OR xx'
    user_name: a string in form of 'xxx OR xxx OR xxx'
    max_results: number of return
    """
    url = "https://api.twitter.com/2/tweets/search/all" # Tweets information
    params = {'query': '(' + keywords + ') ('+'from:'+ username + ')' + ' -is:reply' + ' lang:en',
                    'start_time': start_time,
                    'end_time': end_time_url,
                    'max_results': max_results,
                   'tweet.fields': 'created_at,public_metrics,conversation_id',
                   'next_token': token }
        
    tweets_response = connect_to_endpoint(url, headers, params)
    print(tweets_response)
    df_final = pd.json_normalize(tweets_response['data'])
    while True:
        try:
            token = tweets_response['meta']['next_token']
        except:
            token = None
        if token is None:
            break
        params['next_token'] = token
        tweets_response = connect_to_endpoint(url, headers, params)
        tmp = pd.json_normalize(tweets_response['data'])
        df_final = pd.concat([df_final, tmp], ignore_index=True)
        
    columns = {'created_at':'joined_time',
                   'public_metrics.retweet_count':'retweet_count',
                   'public_metrics.reply_count':'reply_count',
                   'public_metrics.like_count':'like_count', 
                   'public_metrics.quote_count':'quote_count',
                   'public_metrics.id':'id',
                   }
    df_final['is_reply_to_user'] = 0
    df_final['user_id'] = id
    df_final.rename(columns = columns, inplace=True)
    df_final.to_csv('../../../data/tweets/tweets_data_final.csv', mode='a', index=False, header=False)
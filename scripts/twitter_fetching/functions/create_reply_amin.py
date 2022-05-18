from asyncio import new_event_loop
import pandas as pd
from connect_to_endpoint_amin import connect_to_endpoint

def reply_url(to_user, conversation_id, max_results, start_time, end_time, headers, token):
    """
    to_user: the user who tweet
    conversation_id: the conversation_id of the tweet
    max_result: number of return
    """ 
    url = "https://api.twitter.com/2/tweets/search/all" # Tweets information
    params = {'query': '(conversation_id:'+ conversation_id + ') ( ' + 'to:' + to_user + ')' ,
                    'max_results': max_results,
                    'start_time': start_time,
                    'end_time': end_time,
                    'expansions': 'in_reply_to_user_id',
                   'tweet.fields': 'created_at,public_metrics,conversation_id',
                   'next_token': token}
    
    replies_response = connect_to_endpoint(url, headers, params)
    df_final = pd.json_normalize(replies_response['data'])
    
    while True:
        try:
            token = replies_response['meta']['next_token']
        except:
            token = None
        if token is None:
            break
        params['next_token'] = token
        replies_response = connect_to_endpoint(url, headers, params)
        tmp = pd.json_normalize(replies_response['data'])
        df_final = pd.concat([df_final, tmp], ignore_index=True)
        
    new = {'created_at':'joined_time',
                   'in_reply_to_user_id': 'related_user_id',
                   'public_metrics.retweet_count':'retweet_count',
                   'public_metrics.reply_count':'reply_count',
                   'public_metrics.like_count':'like_count', 
                   'public_metrics.quote_count':'quote_count',
                   }
    df_final.rename(columns = new, inplace=True)
    df_final = df_final.iloc[df_final['like_count'].nlargest(n=10).index]
    df_final['is_reply_to_user'] = 1
    df_final.to_csv('../../../data/tweets/replies_data_final.csv', mode='a', index=False, header=False)
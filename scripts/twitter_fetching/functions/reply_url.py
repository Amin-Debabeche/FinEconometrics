import pandas as pd
import connect_to_endpoint
import sys

def create_reply_url(to_user, conversation_id, max_results, start_time, end_time):
    """
    to_user: the user who tweet
    conversation_id: the conversation_id of the tweet
    max_result: number of return
    """
    
    search_url = "https://api.twitter.com/2/tweets/search/all" # Tweets information
    query_params = {'query': '(conversation_id:'+ conversation_id + ') ( ' + 'to:' + to_user + ')' ,
                    'max_results': max_results,
                    'start_time': start_time,
                    'end_time': end_time,              # one day extension of replies
                    'expansions': 'in_reply_to_user_id',
                   'tweet.fields': 'created_at,public_metrics,conversation_id'}
    return (search_url, query_params)

if __name__ == "__main__":
    to_user = sys.argv[1]
    conversation_id = sys.argv[2]
    start_time = sys.argv[3]
    end_time = sys.argv[4]
    headers = sys.argv[5]
    
    replies_url = create_reply_url(to_user, conversation_id, 300, start_time, end_time)
    replies_response = connect_to_endpoint(replies_url[0], headers, replies_url[1])
    df_final = pd.json_normalize(replies_response['data'])
    while True:
        next_token = replies_response['meta']['next_token']
        if next_token is None:
            break
        replies_response = connect_to_endpoint(replies_url[0], headers, replies_url[1], next_token = next_token)
        tmp = pd.json_normalize(replies_response['data'])
        df_final = pd.concat([df_final, tmp], ignore_index=True)
    columns = {'id': 'related_user_id',
                   'created_at':'joined_time',
                   'in_reply_to_user_id': 'related_user_id',
                   'public_metrics.retweet_count':'retweet_count',
                   'public_metrics.reply_count':'reply_count',
                   'public_metrics.like_count':'like_count', 
                   'public_metrics.quote_count':'quote_count',
                   'public_metrics.id':'id',
                   }
    df_final[df_final['like_count'].nlargest(n=10)]
    df_final['is_reply_to_user'] = 1
    df_final.rename(columns = columns, inplace=True)
    df_final.to_csv('replies_data_final.csv',index=False)
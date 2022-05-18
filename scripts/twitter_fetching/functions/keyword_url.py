import pandas as pd
import connect_to_endpoint
import sys

def keyword_url(keyword, user_name, max_results, start_time, end_time_url):
    """
    Search tweets based on keyword and username
    
    keyword: a string in form of 'xx OR xx OR xx'
    user_name: a string in form of 'xxx OR xxx OR xxx'
    max_results: number of return
    """
    search_url = "https://api.twitter.com/2/tweets/search/all" # Tweets information
    query_params = {'query': '(' + keyword + ') ('+'from:'+ user_name + ')' + ' -is:reply' + ' lang:en',
                    'start_time': start_time,
                    'end_time': end_time_url,
                    'max_results': max_results,
                   'tweet.fields': 'created_at,public_metrics,conversation_id'}

    return (search_url, query_params)

if __name__ == "__main__":
    keywords = sys.argv[1]
    username = sys.argv[2]
    start_time = sys.argv[4]
    end_time = sys.argv[5]
    headers = sys.argv[6]
    id = sys.argv[7]

    tweets_url = keyword_url(keywords, username, 500, start_time, end_time)
    tweets_response = connect_to_endpoint(tweets_url[0], headers, tweets_url[1])
    df_final = pd.json_normalize(tweets_response['data'])
    while True:
        next_token = tweets_response['meta']['next_token']
        if next_token is None:
            break
        tweets_response = connect_to_endpoint(tweets_url[0], headers, tweets_url[1], next_token = next_token)
        tmp = pd.json_normalize(tweets_response['data'])
        df_final = pd.concat([df_final, tmp], ignore_index=True)
    columns = {'id': 'related_user_id',
                   'created_at':'joined_time',
                   'public_metrics.retweet_count':'retweet_count',
                   'public_metrics.reply_count':'reply_count',
                   'public_metrics.like_count':'like_count', 
                   'public_metrics.quote_count':'quote_count',
                   'public_metrics.id':'id',
                   }
    df_final['is_reply_to_user'] = 0
    df_final['related_user_id'] = id
    df_final.rename(columns = columns, inplace=True)
    df_final.to_csv('tweets_data_final.csv',index=False)
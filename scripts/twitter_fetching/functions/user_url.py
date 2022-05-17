import pandas as pd
import connect_to_endpoint

def user_url(name_list):
    """
    name_list: a string in form of 'xx1,xx2,xx3'
    """
    search_url = "https://api.twitter.com/2/users/by" # User information
    query_params = {'usernames': name_list,
                     'user.fields': 'created_at,public_metrics'}
    return (search_url, query_params)

if __name__ == "__main__":
    TOKEN = 'AAAAAAAAAAAAAAAAAAAAAKHzbwEAAAAANrBlqwYokl3ttFARZ4ZmiSD7Bw0%3DRa8THgCyIJMa416ckXp3dLfyC4JgfsugJPgLkRT802r0hynEoy'
    headers = {"Authorization": f"Bearer {TOKEN}"}
    df = pd.read_json('../../features/btc_influencers.json')
    df = df.nick.str.replace('@','')
    num = len(df) % 100
    for i in range(num):
        tmp = df[100*i:100*(i+1)]
        user_url = user_url(tmp.nick)
        user_response = connect_to_endpoint(user_url[0], headers, user_url[1])
        df_final = pd.json_normalize(user_response['data'])
        columns = {'id': 'related_user_id',
                   'created_at':'joined_time',
                   'public_metrics.followers_count':'followers_count',
                   'public_metrics.following_count':'tweet_count',
                   'public_metrics.tweet_count':'tweet_count', 
                   'public_metrics.listed_count':'listed_count',
                   }
        df_final.rename(columns = columns, inplace=True)
        #df.drop(columns=['public_metrics'], inplace = True)
        df_final.to_csv('user_data_final.csv', mode='a', index=False, header=False)
    

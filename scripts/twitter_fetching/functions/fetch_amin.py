# %%
from keyword_amin import keyword_url
from create_reply_amin import reply_url
import datetime
import pandas as pd
from tqdm import tqdm

## SETUPS ##
keywords = 'btc OR BTC OR Btc OR xbt OR XBT OR bitcoin OR bitcoins OR BITCOIN OR Bitcoin'
TOKEN = 'AAAAAAAAAAAAAAAAAAAAAKHzbwEAAAAANrBlqwYokl3ttFARZ4ZmiSD7Bw0%3DRa8THgCyIJMa416ckXp3dLfyC4JgfsugJPgLkRT802r0hynEoy'
headers = {"Authorization": f"Bearer {TOKEN}"}
token = None
max_results = 500

user_data = pd.read_csv('../../../data/user_info/user_data.csv')
users = user_data[['username', 'related_user_id']]
done = pd.read_csv('../../../data/user_info/done.csv')

## DATES ##
today = datetime.date.today()
start_time = (today - datetime.timedelta(weeks=4)).strftime(format='%Y-%m-%dT00:00:00.000Z')
end_time = (today - datetime.timedelta(days=4)).strftime(format='%Y-%m-%dT00:00:00.000Z')
end_time_url = today.strftime(format='%Y-%m-%dT00:00:00.000Z')

for l in tqdm(range(len(users[:1]))):
    username = users.username[l]
    if username in done.username.values:
        print(username)
        continue
    done = done.append({'username':username} ,ignore_index=True)
    id = users.related_user_id[l]
    keyword_url(keywords, username, max_results, start_time, end_time, headers, id, token)
    done.to_csv('../../../data/user_info/done.csv', mode='a', index=False, header=False)
    
    print('finished')

tweets_data = pd.read_csv('../../../data/tweets/tweets_data_final.csv')
tweets = tweets_data[['conversation_id', 'related_user_id.1']].astype(str)  
for l in tqdm(range(len(tweets[:1]))):
    to_user = tweets['related_user_id.1'][l]
    conversation_id = tweets.conversation_id[l]
    reply_url(to_user, conversation_id, 300, start_time, end_time_url, headers, token)


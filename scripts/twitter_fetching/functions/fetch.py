import keyword_url
import reply_url
import tqdm
from datetime import datetime
import pandas as pd


## SETUPS ##
keywords = 'btc OR BTC OR Btc OR xbt OR XBT OR bitcoin OR bitcoins OR BITCOIN OR Bitcoin'
TOKEN = 'AAAAAAAAAAAAAAAAAAAAAKHzbwEAAAAANrBlqwYokl3ttFARZ4ZmiSD7Bw0%3DRa8THgCyIJMa416ckXp3dLfyC4JgfsugJPgLkRT802r0hynEoy'
headers = {"Authorization": f"Bearer {TOKEN}"}

user_data = pd.read_csv('../../user_data.csv',)
users = user_data['name', 'related_user_id']

## DATES ##
today = datetime.date.today()
start_time = today - datetime.timedelta(month=1)
end_time = today - datetime.timedelta(days=4)
end_time_url = today

for user in tqdm(users):
    username = user.name
    id = user.related_user_id
    keyword_url(keywords, username, 500, start_time, end_time, headers, id)
    
tweets_data = pd.read_csv('../../twitter_data.csv',)
tweets = tweets_data['conversation_id', 'related_user_id']

for tweet in tqdm(tweets):
    to_user = tweet.related_user_id
    conversation_id = tweet.conversation_id
    reply_url(to_user, conversation_id, 300, start_time, end_time_url, headers)

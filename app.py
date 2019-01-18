import os
import twitter

from dotenv import load_dotenv
from tweet_generator import generate_tweet

def delete_tweet(api, screen_name):
    statuses = api.GetUserTimeline(screen_name=screen_name)
    for s in statuses:
        print(s.text, s.created_at)
        api.DestroyStatus(s.id)

if __name__ == "__main__":
    dotenv_path = os.path.dirname(__file__) + '.env'
    load_dotenv(dotenv_path)

    api = twitter.Api(
        consumer_key=os.environ.get('CONSUMER_KEY'),
        consumer_secret=os.environ.get('CONSUMER_SECRET'),
        access_token_key=os.environ.get('ACCESS_TOKEN'),
        access_token_secret=os.environ.get('ACCESS_SECRET')
    )

    num = 1
    for _ in range(num):
        text = generate_tweet()
        status = api.PostUpdate(text)
        print(status)
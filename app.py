import os
import twitter

from dotenv import load_dotenv
from tweet_generator import generate_tweet

if __name__ == "__main__":
    dotenv_path = os.path.dirname(__file__) + '.env'
    load_dotenv(dotenv_path)

    api = twitter.Api(
        consumer_key=os.environ.get('CONSUMER_KEY'),
        consumer_secret=os.environ.get('CONSUMER_SECRET'),
        access_token_key=os.environ.get('ACCESS_TOKEN'),
        access_token_secret=os.environ.get('ACCESS_SECRET')
    )

    text = generate_tweet()
    status= api.PostUpdate(text)
    print(status)

import csv


from const import TWEET_SOURCE_FILE_NAME


def random_pick_one():
    with open(TWEET_SOURCE_FILE_NAME, 'r') as f:
        reader = csv.reader(f)
        return random.choice(list(reader))


def format_for_tweet(source):
    author = source[0]
    title = source[1]
    quote = source[2]
    return f"{quote}\n\n{author}『{title}』"


def generate_tweet():
    picked_source = random_pick_one()
    return format_for_tweet(picked_source)


if __name__ == "__main__":
    tweet = generate_tweet()
    print(tweet)

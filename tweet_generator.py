import json
import random
import string
import csv

from ese_bungo_generator import generate_ese_bungo_all
from const import TWEET_SOURCE_FILE_NAME

# twitter のソースに使う用
# deploy先でmecab-python3が使えないので、暫定対応
def output_ese_bungo_to_csv(num=1, keep_title_author_consistency=False):
    _, results = generate_ese_bungo_all(num)
    
    with open(TWEET_SOURCE_FILE_NAME, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(results)

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
    output_ese_bungo_to_csv(120)
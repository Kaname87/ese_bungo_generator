import MeCab
def create_tagger():
    tagger = MeCab.Tagger ("-Ochasen") 
    tagger.parse('')
    return tagger

def is_noun(part):
    return '名詞-一般' in part or '名詞-固有' in part or '名詞-数' in part or '名詞-サ変接続' in part

def has_part_length(word_detail):
    return len(word_detail) >= 4
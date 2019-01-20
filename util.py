import MeCab
def create_tagger():
    tagger = MeCab.Tagger ("-Ochasen") 
    tagger.parse('')
    return tagger

def is_noun(part):
    # '名詞-サ変接続' は 「翻訳する」の「翻訳」など
    # '名詞-非自立-副詞可能'は「人の上」のように「の」あとの「上」など
    return '名詞-一般' in part \
        or '名詞-固有' in part \
        or '名詞-数' in part \
        or '名詞-サ変接続' in part \
        or '名詞-非自立-副詞可能' in part

def has_part_length(word_detail):
    return len(word_detail) >= 4
import MeCab


def create_tagger():
    tagger = MeCab.Tagger("-Ochasen")
    tagger.parse('')
    return tagger


def is_target_noun(part):
    # 全ての名詞を対象にはしない。
    # 接頭詞-名詞接続 「老夫婦」の「老」（これは続く単語がすべて名詞なら対象にしてもいいが、現在はそのチェックなし）
    # 名詞-接尾-一般 「反逆罪」の「罪」
    # 名詞-接尾-形容動詞語幹 「がち」
    # 名詞-代名詞-一般 「これ」
    # 名詞-副詞可能「正午」「ここ」など
    # などは単体で役割の違うものに変換すると文がくずれる可能性が高いので対象外

    # '名詞-サ変接続'「翻訳する」の「翻訳」など
    # '名詞-非自立-副詞可能'「人の上」のように「の」あとの「上」など
    # '名詞-形容動詞語幹' 「不滅 」「幸福」など
    return '名詞-一般' in part \
        or '名詞-固有' in part \
        or '名詞-数' in part \
        or '名詞-サ変接続' in part \
        or '名詞-非自立-副詞可能' in part \
        or '名詞-形容動詞語幹' in part


def has_part_length(word_detail):
    return len(word_detail) >= 4

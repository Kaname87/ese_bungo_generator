# -*- coding: utf-8 -*-
import MeCab


def create_tagger():
    tagger = MeCab.Tagger("-Ochasen")
    tagger.parse('')
    return tagger


def in_target_noun_type(part):
    '''
    対象の名詞かチェック。
    全ての名詞を対象にはしない。
    接頭詞-名詞接続 「老夫婦」の「老」（これは続く単語がすべて名詞なら対象にしてもいいが、現在はそのチェックなし）
    名詞-接尾-一般 「反逆罪」の「罪」
    名詞-接尾-形容動詞語幹 「がち」
    名詞-代名詞-一般 「これ」
    名詞-副詞可能「正午」「ここ」など
    などは単体で役割の違うものに変換すると文がくずれる可能性が高いので対象外

    '名詞-サ変接続'「翻訳する」の「翻訳」など
    '名詞-非自立-副詞可能'「人の上」のように「の」あとの「上」など
    '名詞-形容動詞語幹' 「不滅 」「幸福」など
    '''
    return '名詞-一般' in part \
        or '名詞-固有' in part \
        or '名詞-数' in part \
        or '名詞-サ変接続' in part \
        or '名詞-非自立-副詞可能' in part \
        or '名詞-形容動詞語幹' in part


def has_part_length(word_detail):
    '''
    品詞がある長さかチェック
    '''
    return len(word_detail) >= 4


def is_target_noun(parsed_text):
    parsed_text_detail = parsed_text.split('\t')
    return has_part_length(parsed_text_detail) and in_target_noun_type(parsed_text_detail[3])


def is_independent_noun(post_target_parsed_text):
    '''
    候補の単語の次の単語（post_similar_word）判定
    名詞＋助詞、という類義語のパターンは文章が崩れるのでスキップ
    ("人" => "人が" や、"桜" => "桜の" など）
   「基本的」のような「的」というパターンも名詞ではないのでスキップ
    '''
    if has_part_length(post_target_parsed_text):
        part = post_target_parsed_text.split('\t')[3]
        if '助詞' in part:
            return False
        # 「-的」を対象外に
        if '名詞-接尾-形容動詞語幹' in part:
            return False
    return True


def get_noun_list(text):
    tagger = create_tagger()
    parsed_text_list = tagger.parse(text).split('\n')
    return [parsed_text.split('\t')[0] for parsed_text in parsed_text_list if is_target_noun(parsed_text)]


if __name__ == "__main__":
    text = '俺がおまえで、お前が俺で'
    out = get_noun_list(text)
    print(out)

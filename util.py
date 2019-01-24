import MeCab
import random
import string
from gensim.models import KeyedVectors


def load_model(path):
    return KeyedVectors.load_word2vec_format(path, binary=True)


def create_tagger(tagger_name="-Ochasen"):
    '''
    タガー作成
    '''
    tagger = MeCab.Tagger(tagger_name)
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


def is_target_noun(tab_divided_word_token):
    '''
    変換対象の名詞かどうかチェック
    '''
    text_token_list = tab_divided_word_token.split('\t')
    return has_part_length(text_token_list) and in_target_noun_type(text_token_list[3])


def is_independent_noun(next_word_tab_divided_word_token):
    '''
    候補の名詞の次の単語判定
    名詞＋助詞、という類義語のパターンは文章が崩れるのでスキップ
    ("人" => "人が" や、"桜" => "桜の" など）
   「基本的」のような「的」というパターンも名詞ではないのでスキップ
    '''
    if has_part_length(next_word_tab_divided_word_token):
        part = next_word_tab_divided_word_token.split('\t')[3]
        if '助詞' in part:
            return False
        # 「-的」を対象外に
        if '名詞-接尾-形容動詞語幹' in part:
            return False
    return True


def get_noun_list(text):
    tagger = create_tagger()
    tab_divided_word_token_list = tagger.parse(text).split('\n')
    return [tab_divided_word_token.split('\t')[0] for tab_divided_word_token in tab_divided_word_token_list if is_target_noun(tab_divided_word_token)]


def generate_unique_place_holder(placeholder_dict):
    '''
    文章の置き換え必要な一意のplaceholderを生成する
    パラメータのplaceholder_dictはすでに生成されたplaceholderをkeyに持つ
    '''
    placeholder_base = '_PLACE_HOLDER'
    while(True):
        placeholder = placeholder_base + \
            "".join([random.choice(string.digits) for _ in range(15)])
        if placeholder not in placeholder_dict.keys():
            break
    return placeholder


def diff_list(a, b):
    return list(set(a)-set(b))


if __name__ == "__main__":
    text = '俺がおまえで、お前が俺で'
    out = get_noun_list(text)
    print(out)

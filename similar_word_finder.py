import json
import csv
import random
from gensim.models import KeyedVectors

from const import ORIGINAL_NOVEL_FILE, NAME_CHARCTER_LIST_FILE, NOUN_LIST_FILE, WORD2VEC_MODEL_PATH
from util import is_noun, has_part_length, create_tagger


def load_model():
    return KeyedVectors.load_word2vec_format(WORD2VEC_MODEL_PATH, binary=True)


def find_similar_word(model, word, topn=10):
    similar_word_list = []
    try:
        similar_word_list = model.most_similar(f'{word}', topn=topn)
    except Exception as e:
        print(f'Exception is raiesd when finding similar word of {word}')
        print(type(e), e)

    return similar_word_list


def create_similar_noun_dict(model, tagger, target_noun_list, topn=10):
    similar_noun_results = {}
    for target_noun in target_noun_list:
        similar_word_list = find_similar_word(model, target_noun, topn)
        for similar_word_with_similarity in similar_word_list:
            similar_word = similar_word_with_similarity[0]

            # 余計な括弧を削除
            similar_word = similar_word.strip('[').strip(']')

            # 同じ単語はスキップ
            if similar_word == target_noun:
                continue
            # _(単位) や_(キャラクター) は、ふくまない. Category:xxxも。
            if "_(" in similar_word or "Category:" in similar_word:
                continue

            similar_word_details = tagger.parse(similar_word).split('\n')
            similar_word_detail = similar_word_details[0]

            # Length Check
            if not has_part_length(similar_word_detail):
                continue
            # 品詞 Check
            part = similar_word_detail.split('\t')[3]
            if not is_noun(part):
                continue

            # 候補の単語の次も文字判定
            # 名詞＋助詞、という類義語のパターンは文章が崩れるのでスキップ
            # ("人" => "人が" や、"桜" => "桜の" など）
            # 「基本的」のような「的」というパターンも名詞ではないのでスキップ
            post_similar_word_detail = similar_word_details[1]
            if has_part_length(post_similar_word_detail):
                post_part = post_similar_word_detail.split('\t')[3]
                if '助詞' in post_part:
                    continue
                # 「-的」を対象外に
                if '名詞-接尾-形容動詞語幹' in post_part:
                    continue

            # 不愉快な差別的文章になりそうなものを排除。
            # 発見ベースで随時リスト追加
            if similar_word in ['中国人', '韓国人', 'アメリカ人']:
                continue

            if target_noun in similar_noun_results:
                similar_words = similar_noun_results[target_noun]
                if similar_word not in similar_words:
                    similar_words.append(similar_word)
                    similar_noun_results[target_noun] = similar_words
            else:
                similar_noun_results[target_noun] = [similar_word]

    return similar_noun_results


def replace_by_similar_word(target_text, similar_word_dict):
    replaced_text = target_text
    for target_word, similar_words in similar_word_dict.items():
        similar_word = random.choice(similar_words)
        replaced_text = replaced_text.replace(target_word, similar_word)

    return replaced_text


def create_noun_list(parsed_text):
    noun_list = []
    for parsed_word in parsed_text:
        word_detail = parsed_word.split('\t')
        if not has_part_length(word_detail):
            continue

        word = word_detail[0]
        part = word_detail[3]
        if is_noun(part):
            noun_list.append(word)

    return noun_list


def read_and_parse_json(model, tagger):
    name_char_dict = {}
    noun_dict = {}

    dictdump = {}
    with open(ORIGINAL_NOVEL_FILE) as f:
        dictdump = json.loads(f.read())

    for author, novel_list in dictdump.items():
        # Author
        author_char_list = list(author)
        author_results = create_similar_noun_dict(
            model, tagger, author_char_list, 7)
        name_char_dict.update(author_results)

        for novel in novel_list:
            # 名詞のリストをつくるのに、title, quotes の区別不要なので、マージ
            target_list = [novel['title']] + novel['quotes']

            for target in target_list:
                parsed_text = tagger.parse(target).split('\n')
                noun_list = create_noun_list(parsed_text)
                noun_results = create_similar_noun_dict(
                    model, tagger, noun_list, 8)
                noun_dict.update(noun_results)

    return name_char_dict, noun_dict


def write_to_json(filepath, result_dict):
    result_json = json.dumps(result_dict, ensure_ascii=False)
    with open(filepath, "w") as f:
        f.write(result_json)


def output_to_json():
    model = load_model()
    tagger = create_tagger()

    name_char_dict, noun_dict = read_and_parse_json(model, tagger)

    write_to_json(NAME_CHARCTER_LIST_FILE, name_char_dict)
    write_to_json(NOUN_LIST_FILE, noun_dict)


if __name__ == "__main__":
    output_to_json()
    print('Done')

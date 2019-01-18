import json
import random
import string

from util import is_noun, has_part_length, create_tagger
from const import ORIGINAL_NOVEL_FILE, NAME_CHARCTER_LIST_FILE, NOUN_LIST_FILE, ESE_BUNGO_LIST


def read_json_to_dict(file_path):
    res = {}
    with open(file_path) as f:
        res = json.loads(f.read())
    return res

# 切り下げ. 最大で名前の半分を変更


def get_max_replace_char_num(name):
    return len(name) // 2


def create_replace_char_idx_list(name):
    replace_char_idx_list = []

    replace_char_num = get_max_replace_char_num(name)
    name_len_range = range(len(name))

    while (len(replace_char_idx_list) < replace_char_num):
        char_idx = random.choice(name_len_range)
        if char_idx in replace_char_idx_list:
            continue
        replace_char_idx_list.append(char_idx)
    return replace_char_idx_list


def generate_name(author_name):
    name_char_dict = read_json_to_dict(NAME_CHARCTER_LIST_FILE)
    replace_char_idx_list = create_replace_char_idx_list(author_name)

    replaced_name = ''
    for idx, name_char in enumerate(author_name):
        if idx in replace_char_idx_list:
            similar_char_list = name_char_dict[name_char]
            replaced_name += random.choice(similar_char_list)
        else:
            # 置き換え対処じゃないのはそのまま追加
            replaced_name += name_char

    return replaced_name


def generate_unique_place_holder(placeholder_dict):
    placeholder_base = '_PLACE_HOLDER'
    while(True):
        placeholder = placeholder_base + \
            "".join([random.choice(string.digits) for _ in range(15)])
        if placeholder not in placeholder_dict.keys():
            break
    return placeholder


def replace_noun_by_similar_word(target_text, noun_list, tagger, used_word):
    WORD_IDX = 0
    PART_IDX = 3

    # 名詞を類義語で置き換える。
    # 置き換え後の単語の一部が再度別の類義後に置き換えられる問題（「天」を「天人」に置き換えた後に「人」が別のに置き換えられる問題）
    # をふせぐため、直接置き換えるのではなく、一度ユニークなプレースホルダーに置き換えておく。
    # 全部のプレースホルダー置き換え完了後、プレースホルダーを対応する類義語に置き換える。

    # 置き換え結果テキストを初期化
    replaced_text = target_text

    # 一度置き換えた単語保持用
    replaced_word_list = []

    # placeholder と類義語の対応dict
    placeholder_similar_word_dict = {}

    parsed_text_list = tagger.parse(target_text).split('\n')

    # 長い単語から走査するためソート。短いものから置換してしまうと、別の単語の一部が先に置換されてしまう。「怪人」と「人」など。
    # ソートのために品詞を持ってるものだけでフィルター (EOSなどは含まない)
    has_part_list = [parsed_word for parsed_word in parsed_text_list if has_part_length(
        parsed_word.split('\t'))]
    sorted_text_list = sorted(has_part_list, key=lambda parsed_word: len(
        parsed_word.split('\t')[WORD_IDX]), reverse=True)

    for parsed_word in sorted_text_list:

        word_detail = parsed_word.split('\t')
        part = word_detail[PART_IDX]

        # 名詞のみ対象
        if is_noun(part):
            word = word_detail[WORD_IDX]
            if word not in noun_list:
                continue

            #  一文で同じ単語を一度置き換えた単語保持。なんども置き換えない
            if word in replaced_word_list:
                continue

            similar_word_list = noun_list[word]
            similar_word = ''
            # 一度つかった置き換えパターンはおなじのをつかう
            if word in used_word.keys():
                similar_word = used_word[word]
            else:
                similar_word = random.choice(similar_word_list)
                used_word[word] = similar_word

            # プレースホルダーで置き換え
            placeholder = generate_unique_place_holder(
                placeholder_similar_word_dict)
            replaced_text = replaced_text.replace(word, placeholder)
            # 一度置き換えた単語保持
            placeholder_similar_word_dict[placeholder] = similar_word
            replaced_word_list.append(word)

    # プレースホルダー 置き換え
    for placeholder, similar_word in placeholder_similar_word_dict.items():
        replaced_text = replaced_text.replace(placeholder, similar_word)

    return replaced_text


def generate_ese_bungo(num=1):
    tagger = create_tagger()
    source_dict = read_json_to_dict(ORIGINAL_NOVEL_FILE)
    noun_list_dict = read_json_to_dict(NOUN_LIST_FILE)

    results = []
    loop_cnt = 0

    orginal_list = []
    for author_name, novel_list in source_dict.items():
        for novel in novel_list:
            used_title_author = {}
            title = novel['title']
            # for quote in novel['quotes']:
            for q_idx in range(len(novel['quotes'])):
                quote = novel['quotes'][q_idx]

                orginal_list.append([author_name, title, quote, novel['url']])
                orginal_list_idx = len(orginal_list) - 1
                used_quote = []
                for _ in range(num):
                    loop_cnt = loop_cnt + 1

                    # 1つの作品（タイトル＋クオート）の中で、おなじ単語は同じように変換するようにused_wordに保持。
                    # 『走れメロス』の「メロスは激怒した。」のようにタイトル中の単語が本文中で使われてる時、
                    # 別々に変換すると面白みが減るため
                    used_word = {}

                    generated_quote = replace_noun_by_similar_word(
                        quote, noun_list_dict, tagger, used_word)
                    # 同じQuoteは省く。なんども同じの見ても退屈なので(デモサイト用)
                    if generated_quote in used_quote:
                        continue
                    else:
                        used_quote.append(generated_quote)

                    generated_title = replace_noun_by_similar_word(
                        title, noun_list_dict, tagger, used_word)
                    generated_name = ''
                    if generated_title in list(used_title_author.keys()):
                        generated_name = used_title_author[generated_title]
                    else:
                        generated_name = generate_name(author_name)
                        used_title_author[generated_title] = generated_name

                    # print(used_word)
                    print(author_name, title, quote)
                    print('')
                    print(generated_name, generated_title, generated_quote)
                    print('---')
                    fake = [generated_name, generated_title,
                            generated_quote, orginal_list_idx]
                    results.append(fake)

    print('loop_cnt:', loop_cnt)
    print('total:', len(results))

    return orginal_list, results


def output_ese_bungo_to_js(num):
    orginal_list, results = generate_ese_bungo(num)

    result_json = json.dumps(results, ensure_ascii=False)
    orginal_list_json = json.dumps(orginal_list, ensure_ascii=False)

    # htmlで使うようにjsをつくる
    original_list = 'const ORIGINAL_LIST= ' + orginal_list_json + ';'
    ese_bungo_list = 'const ESE_BUNGO_LIST= ' + result_json + ';'

    with open(ESE_BUNGO_LIST, "w") as f:
        f.write(original_list + '\n')
        f.write(ese_bungo_list)


if __name__ == "__main__":
    output_ese_bungo_to_js(60)
    # output_ese_bungo_to_js(15000)

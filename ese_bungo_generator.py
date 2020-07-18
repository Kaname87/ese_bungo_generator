import json
import csv
import random

# from util import create_tagger, is_target_noun
# from const import ORIGINAL_NOVEL_FILE, NAME_CHARCTER_LIST_FILE, SIMILAR_NOUN_LIST_FILE, ESE_BUNGO_LIST, TWEET_SOURCE_FILE_NAME
import util
import const
import argparse


def read_json_to_dict(file_path):
    res = {}
    with open(file_path) as f:
        res = json.loads(f.read())
    return res


def get_max_replace_char_num(name):
    '''
    名前のうち何文字を変換するか取得
    '''
    # 切り下げ。 最低でも名前の半分を変更
    return len(name) // 2


def create_replace_char_idx_list(name):
    '''
    名前の置き換える文字のindexリスト作成
    '''
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
    '''
    名前の文字を置き換えて、新しい文字を生成
    名前の全ての文字を置き換えるのではなく、一部のみを置き換える。
    全部を置き換えると、元ネタと離れすぎるため
    '''
    name_char_dict = read_json_to_dict(const.NAME_CHARCTER_LIST_FILE)
    # 置き換え対象の文字のindexを取得
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


def replace_noun_by_similar_word(target_text, similar_noun_list, tagger, used_word):
    '''
    名詞を類義語で置き換える。
    置き換え後の単語の一部が再度別の類義後に置き換えられる問題（「天」を「天人」に置き換えた後に「人」が別のに置き換えられる問題）
    をふせぐため、直接置き換えるのではなく、一度ユニークなプレースホルダーに置き換えておく。
    全部のプレースホルダー置き換え完了後、プレースホルダーを対応する類義語に置き換える。
    '''
    WORD_IDX = 0

    # 置き換え結果テキストを初期化
    replaced_text = target_text

    # 一度置き換えた単語保持用
    replaced_word_list = []

    # placeholder と類義語の対応dict
    placeholder_similar_word_dict = {}

    tab_divided_word_token_list = tagger.parse(target_text).split('\n')

    # 長い単語から走査するためソート。短いものから置換してしまうと、別の単語の一部が先に置換されてしまう。「怪人」と「人」など。
    # ソートのために先に名詞のものだけにでフィルター (EOSなどは含まない)
    noun_tab_divided_word_token_list = [tab_divided_word_token for tab_divided_word_token in tab_divided_word_token_list if util.is_target_noun(
        tab_divided_word_token)]
    sorted_tab_divided_word_token_list = sorted(noun_tab_divided_word_token_list, key=lambda tab_divided_word_token: len(
        tab_divided_word_token.split('\t')[WORD_IDX]), reverse=True)

    for tab_divided_word_token in sorted_tab_divided_word_token_list:
        word_token_list = tab_divided_word_token.split('\t')
        word = word_token_list[WORD_IDX]
        if word not in similar_noun_list:
            continue

        #  一文で同じ単語を一度置き換えた単語保持。なんども置き換えない
        if word in replaced_word_list:
            continue

        similar_word_list = similar_noun_list[word]
        similar_word = ''
        # 一度つかった置き換えパターンはおなじのをつかう
        if word in used_word.keys():
            similar_word = used_word[word]
        else:
            similar_word = random.choice(similar_word_list)
            used_word[word] = similar_word

        # プレースホルダーで置き換え
        placeholder = util.generate_unique_place_holder(
            placeholder_similar_word_dict)
        replaced_text = replaced_text.replace(word, placeholder)
        # 一度置き換えた単語保持
        placeholder_similar_word_dict[placeholder] = similar_word
        replaced_word_list.append(word)

    # プレースホルダー 置き換え
    for placeholder, similar_word in placeholder_similar_word_dict.items():
        replaced_text = replaced_text.replace(placeholder, similar_word)

    return replaced_text, used_word


def random_generate_ese_bungo_one():
    '''
    一つだけrandomで取得する用
    '''
    tagger = util.create_tagger()
    source_dict = read_json_to_dict(const.ORIGINAL_NOVEL_FILE)
    noun_list_dict = read_json_to_dict(const.SIMILAR_NOUN_LIST_FILE)

    author_name, novel_list = random.choice(list(source_dict.items()))
    novel = random.choice(novel_list)
    title = novel['title']
    quote = random.choice(novel['quotes'])

    used_word = {}
    generated_quote, used_word = replace_noun_by_similar_word(
        quote, noun_list_dict, tagger, used_word)
    generated_title, used_word = replace_noun_by_similar_word(
        title, noun_list_dict, tagger, used_word)
    generated_name = generate_name(author_name)

    print(author_name, title, quote)
    print('')
    print(generated_name, generated_title, generated_quote)
    print('---')

    original = {'author': author_name, 'title': title,
                'quote': quote, 'url': novel['url']}
    generated = {'author': generated_name,
                 'title': generated_title, 'quote': generated_quote}
    return original, generated


def generate_ese_bungo_all(num=1):
    '''
    元データにある文言をnum分だけ変換
    '''
    tagger = util.create_tagger()
    source_dict = read_json_to_dict(const.ORIGINAL_NOVEL_FILE)
    noun_list_dict = read_json_to_dict(const.SIMILAR_NOUN_LIST_FILE)

    results = []
    loop_cnt = 0

    orginal_list = []

    a_c = 0  # 作家数
    n_c = 0  # 作品数
    q_c = 0  # 引用文数
    for author_name, novel_list in source_dict.items():
        a_c += 1
        for novel in novel_list:
            n_c += 1
            title = novel['title']
            # for quote in novel['quotes']:
            for quote in novel['quotes']:
                q_c += 1
                orginal_list.append([author_name, title, quote, novel['url']])
                orginal_list_idx = len(orginal_list) - 1
                used_quote = []
                for _ in range(num):
                    loop_cnt = loop_cnt + 1

                    # 1つの作品（タイトル＋クオート）の中で、おなじ単語は同じように変換するようにused_wordに保持。
                    # 『走れメロス』の「メロスは激怒した。」のようにタイトル中の単語が本文中で使われてる時、
                    # 別々に変換すると面白みが減るため
                    used_word = {}

                    generated_quote, used_word = replace_noun_by_similar_word(
                        quote, noun_list_dict, tagger, used_word)
                    # 同じQuoteは省く。なんども同じの見ても退屈なので(デモサイト用)
                    if generated_quote in used_quote:
                        continue
                    else:
                        used_quote.append(generated_quote)

                    generated_title, used_word = replace_noun_by_similar_word(
                        title, noun_list_dict, tagger, used_word)

                    generated_name = generate_name(author_name)

                    print(author_name, title, quote)
                    print('')
                    print(generated_name, generated_title, generated_quote)
                    print('---')
                    fake = [generated_name, generated_title,
                            generated_quote, orginal_list_idx]
                    results.append(fake)

    print(f'author :{a_c}, novel :{n_c}, quote :{q_c}')
    print('loop_cnt:', loop_cnt)
    print('total:', len(results))

    return orginal_list, results


def output_ese_bungo_to_csv(num=1):
    '''
    twitter のソースに使う用
    deploy先でmecab-python3が使えないので、暫定対応
    tweet作成用ファイルではなくこのファイルにおくのはmecabをつかってるファイルをapp.pyで呼ばないようにするため
    '''
    _, results = generate_ese_bungo_all(num)

    with open(const.TWEET_SOURCE_FILE_NAME, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(results)


def output_ese_bungo_to_js(num=1):
    '''
    デモサイト用に結果をJSファイルで吐き出す
    '''
    orginal_list, results = generate_ese_bungo_all(num)

    result_json = json.dumps(results, ensure_ascii=False)
    orginal_list_json = json.dumps(orginal_list, ensure_ascii=False)

    # htmlで使うようにjsをつくる
    original_list = 'const ORIGINAL_LIST= ' + orginal_list_json + ';'
    ese_bungo_list = 'const ESE_BUNGO_LIST= ' + result_json + ';'

    with open(const.ESE_BUNGO_LIST, "w") as f:
        f.write(original_list + '\n')
        f.write(ese_bungo_list)

def execute():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('action', type=str,  choices=['update_csv', 'update_js'])
    parser.add_argument("-n", "--number", default=100, type=int)

    args = parser.parse_args()

    action = args.action
    number = args.number
    print('Action: ' + action)
    print('Number: ' + str(number))

    if args.action == 'update_csv':
        # For twitter
        output_ese_bungo_to_csv(number)
    elif args.action == 'update_js':
        # For demosite
        output_ese_bungo_to_js(number)

    print('Done')

if __name__ == "__main__":
    execute()


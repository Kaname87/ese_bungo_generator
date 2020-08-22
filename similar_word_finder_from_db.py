import json
import csv
import random
import psycopg2

import util
import const


def read_json_to_dict(file_path):
    res = {}
    with open(file_path) as f:
        res = json.loads(f.read())
    return res

# from web.database import SessionLocal, engine
# from web import models
def get_connect():
    return psycopg2.connect("dbname=ese_bungo user=postgres")

def find_similar_word(model, word, topn=10):
    similar_word_tuple_list = []
    try:
        similar_word_tuple_list = model.most_similar(f'{word}', topn=topn)
    except Exception as e:
        print(f'Exception is raiesd when finding similar word of {word}')
        print(type(e), e)

    return similar_word_tuple_list


def create_similar_noun_dict(model, tagger, target_noun_list, topn=10):
    '''
    名詞をキーに類似名詞の辞書を作成
    '''
    similar_noun_results = {}
    for target_noun in target_noun_list:
        similar_word_tuple_list = find_similar_word(model, target_noun, topn)
        for similar_word_tuple in similar_word_tuple_list:
            similar_word = similar_word_tuple[0]

            # 余計な括弧を削除
            similar_word = util.strip_unnecessary_characters(similar_word)

            # 同じ単語はスキップ
            if similar_word == target_noun:
                continue
            # _(単位) や_(キャラクター) は、ふくまない. Category:xxxも。
            if "_(" in similar_word or "Category:" in similar_word:
                continue

            tab_divided_word_token_list = tagger.parse(
                similar_word).split('\n')
            tab_divided_word_token = tab_divided_word_token_list[0]

            # 名詞のみ
            if not util.is_target_noun(tab_divided_word_token):
                continue

            # 候補の名詞の次の単語判定
            # 名詞として完結してる単語出ない場合つかわない
            next_word_tab_divided_word_token = tab_divided_word_token_list[1]
            if not util.is_independent_noun(next_word_tab_divided_word_token):
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


def create_noun_list(tab_divided_word_token_list):
    noun_list = []
    for tab_divided_word_token in tab_divided_word_token_list:
        if not util.is_target_noun(tab_divided_word_token):
            continue
        word_token_list = tab_divided_word_token.split('\t')
        word = word_token_list[0]
        noun_list.append(word)

    return noun_list


def crate_target_word_dict_similar_char(model, tagger, name_char_topn, noun_topn):
    '''
    変換元小説情報から、
    変換対象になる名前の文字と類似文字の辞書、
    変換対象になる名詞と類似名詞の辞書
    を作成する
    '''
    similar_name_char_dict = {}

    conn = None
    try:
        conn = get_connect()
        cur = conn.cursor()

        # Author
        cur.execute("SELECT name from authors")
        authors = cur.fetchall()
        for author in authors:
            author_name = author[0]
            author_char_list = list(author_name)
            author_results = create_similar_noun_dict(
                model, tagger, author_char_list, name_char_topn)
            similar_name_char_dict.update(author_results)

        cur.close()
        conn.commit()

        return similar_name_char_dict
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def crate_target_word_dict_similar_char_tmp(model, tagger, name_char_topn, noun_topn):
    '''
    変換元小説情報から、
    変換対象になる名前の文字と類似文字の辞書、
    変換対象になる名詞と類似名詞の辞書
    を作成する
    '''
    similar_name_char_dict = {}


    source_dict= read_json_to_dict(const.ORIGINAL_NOVEL_SOURCE_TMP)

    for author_name, data in source_dict.items():
        print('Procss: {}'.format(author_name))
        # Author

        author_char_list = list(author_name)
        author_results = create_similar_noun_dict(
            model, tagger, author_char_list, name_char_topn)
        similar_name_char_dict.update(author_results)

    return similar_name_char_dict


def crate_target_word_dict_similar_noun(model, tagger, name_char_topn, noun_topn):
    '''
    変換元小説情報から、
    変換対象になる名前の文字と類似文字の辞書、
    変換対象になる名詞と類似名詞の辞書
    を作成する
    '''

    similar_noun_dict = {}

    # target_list = []
    conn = None
    try:
        conn = get_connect()
        cur = conn.cursor()

        # Book
        cur.execute("SELECT title from books")
        books = cur.fetchall()
        # print('authos')
        print(books)
        for book in books:
            # 名詞のリストをつくるのに、title, quotes の区別不要なので、マージ
            tab_divided_word_token_list = tagger.parse(book[0]).split('\n')
            noun_list = create_noun_list(tab_divided_word_token_list)
            noun_results = create_similar_noun_dict(
                model, tagger, noun_list, noun_topn)
            similar_noun_dict.update(noun_results)

        # Book
        cur.execute("SELECT text from quotes")
        quotes = cur.fetchall()
        # print('authos')
        print(quotes)
        for quote in quotes:
            # 名詞のリストをつくるのに、title, quotes の区別不要なので、マージ
            tab_divided_word_token_list = tagger.parse(quote[0]).split('\n')
            noun_list = create_noun_list(tab_divided_word_token_list)
            noun_results = create_similar_noun_dict(
                model, tagger, noun_list, noun_topn)
            similar_noun_dict.update(noun_results)

        cur.close()
        conn.commit()

        return similar_noun_dict
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def crate_target_word_dict_similar_noun_tmp(model, tagger, name_char_topn, noun_topn):
    '''
    変換元小説情報から、
    変換対象になる名前の文字と類似文字の辞書、
    変換対象になる名詞と類似名詞の辞書
    を作成する
    '''

    similar_noun_dict = {}

    source_dict= read_json_to_dict(const.ORIGINAL_NOVEL_SOURCE_TMP)

    for _, data in source_dict.items():
        # Book
       for book in data['novels']:
            print('Procss Novel: {}'.format(book['title']))
            tab_divided_word_token_list = tagger.parse(book['title']).split('\n')
            noun_list = create_noun_list(tab_divided_word_token_list)
            noun_results = create_similar_noun_dict(
                model, tagger, noun_list, noun_topn)
            similar_noun_dict.update(noun_results)

            for quote_text in book['quotes']:
                tab_divided_word_token_list = tagger.parse(quote_text).split('\n')
                noun_list = create_noun_list(tab_divided_word_token_list)
                noun_results = create_similar_noun_dict(
                    model, tagger, noun_list, noun_topn)
                similar_noun_dict.update(noun_results)

    return similar_noun_dict

def write_to_json(filepath, result_dict):
    result_json = json.dumps(result_dict, ensure_ascii=False)
    with open(filepath, "w") as f:
        f.write(result_json)


def output_word_list(name_char_topn, noun_topn):
    '''
    JSON出力
    '''
    # name_char_topn, noun_topn は類似度のチューニング用
    model = util.load_model(const.WORD2VEC_MODEL_PATH)
    tagger = util.create_tagger()

    name_char_dict = crate_target_word_dict_similar_char(
        model, tagger, name_char_topn, noun_topn)

    noun_dict = crate_target_word_dict_similar_noun(
        model, tagger, name_char_topn, noun_topn)

    # name_char_dict, noun_dict = crate_target_word_dict(
    #     model, tagger, name_char_topn, noun_topn)

    write_to_json(const.NAME_CHARCTER_LIST_FILE, name_char_dict)
    write_to_json(const.SIMILAR_NOUN_LIST_FILE, noun_dict)



def output_word_list_tmp(name_char_topn, noun_topn):
    '''
    JSON出力
    '''
    # name_char_topn, noun_topn は類似度のチューニング用
    model = util.load_model(const.WORD2VEC_MODEL_PATH)
    tagger = util.create_tagger()

    name_char_dict = crate_target_word_dict_similar_char_tmp(
        model, tagger, name_char_topn, noun_topn)

    noun_dict = crate_target_word_dict_similar_noun_tmp(
        model, tagger, name_char_topn, noun_topn)

    # name_char_dict, noun_dict = crate_target_word_dict(
    #     model, tagger, name_char_topn, noun_topn)

    write_to_json(const.NAME_CHARCTER_LIST_FILE_TMP, name_char_dict)
    write_to_json(const.SIMILAR_NOUN_LIST_FILE_TMP, noun_dict)


def out_put_for_demosite(name_char_topn=7, noun_topn=8):
    '''
    デモサイト用出力
    '''
    # demo サイト用パラメータ
    # name_char_topn = 7
    # noun_topn = 8
    output_word_list(name_char_topn, noun_topn)


def out_put_for_twitter(name_char_topn=8, noun_topn=9):
    '''
    Twitter用出力
    '''
    # name_char_topn = 8
    # noun_topn = 9
    output_word_list(name_char_topn, noun_topn)


if __name__ == "__main__":
    # out_put_for_twitter()
    # models.Base.metadata.create_all(bind=engine)
    # session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
    # session = SessionLocal()
    # authors = session.query(models.Author).all()

    # for author in authors:
    #     print(list(author.name))
    output_word_list(7, 8)
    # output_word_list(8, 9)
    # output_word_list_tmp(7, 8)


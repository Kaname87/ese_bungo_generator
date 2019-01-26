import util


def is_nega_word(word_score):
    '''
    ネガワード時にTrue
    '''
    BASE_SCORE = 0
    return float(word_score) <= BASE_SCORE


def get_pn_dict1():
    '''
    PNディクショナリー（極性辞書）取得。
    東北大 乾・岡崎研究室「日本語評価極性辞書（名詞編)」使用
    '''
    WORD_IDX = 0
    PART_IDX = 2  # 品詞
    SCORE_IDX = 3
    d = {}
    with open("data/pn_dict_source/pn_ja.dic.txt", 'r') as f:
        for line in f.readlines():
            word_details = line.split(':')
            # 名詞編といいつつ名詞意外もあるので、名詞のみ残す
            if word_details[PART_IDX] == '名詞':
                d[word_details[WORD_IDX]] = word_details[SCORE_IDX]
    return d


def get_pn_dict2():
    '''
    PNディクショナリー（極性辞書）取得。
    東工大 高村教授「単語感情極性対応表」使用
    '''
    d = {}
    with open("data/pn_dict_source/pn.csv.m3.120408.trim", 'r') as f:
        for line in f.readlines():
            word_details = line.split('\t')
            score = 0
            if word_details[1] == 'p':
                score = 1
            elif word_details[1] == 'n':
                score = -1
            d[word_details[0]] = score
    return d


def create_nega_to_posi_dict(model, nega_word_list, pn_dict, decorate_word_list, topn=10):
    '''
    ネガワードのポジワードへの変換辞書を作成
    '''

    # デコレーション結果をあとでまとめて見る用の履歴
    decorate_history_list = []

    naga_to_posi_dict = {}
    for nega_word in nega_word_list:
        try:
            for decorate_word in decorate_word_list:
                # すでに別のdecorate_wordがこのネガワードに対応するポジワード発見済みなら
                # 次のネガワードへ
                if nega_word in naga_to_posi_dict.keys():
                    break

                similar_word_list = model.most_similar(
                    positive=[f'{nega_word}', f'{decorate_word}'], topn=topn)

                print('----------')
                print(f'Try to decorate {nega_word} by {decorate_word}')

                for similar_word_tuple in similar_word_list:
                    similar_word = similar_word_tuple[0]

                    similar_word = util.strip_unnecessary_characters(
                        similar_word)

                    if not similar_word in pn_dict.keys():
                        print(f'{similar_word} is not in pn_dict')
                        continue
                    similar_word_score = pn_dict[similar_word]
                    score = pn_dict[similar_word].strip('\n')

                    if not is_nega_word(score):
                        naga_to_posi_dict[nega_word] = similar_word
                        print(
                            f'{nega_word} to {similar_word} decorated by {decorate_word}: {similar_word_score}')
                        decorate_history_list.append(
                            [decorate_word, nega_word, similar_word])
                        break
                    else:
                        print(
                            f'{similar_word} is not posi word: {similar_word_score}')

        except Exception as e:
            print(
                f'Exception is raiesd when finding similar word of {nega_word}')
            print(type(e), e)

    return naga_to_posi_dict, decorate_history_list


def create_nega_word_list(tagger, target_text, pn_dict):
    '''
    文章中のネガワードのリストを生成する
    '''
    nega_word_list = []

    # ここでは語、読み、品詞などがタブ区切りの状態をword_tokensとよぶ
    all_word_tokens_list = tagger.parse(target_text).split('\n')
    for word_tokens in all_word_tokens_list:
        if not util.is_target_noun(word_tokens):
            continue

        target_word = word_tokens.split('\t')[0]

        # 単語の原型が辞書にあるかチェック
        # 読み仮名だと同じ言葉かわからない。
        # また、同じ語でもカタカナや漢字など書き方がことなると検知不可だが、今回はあきらめ
        # 辞書にある単語は全て名詞のはずなので、品詞チェックなし
        if target_word in pn_dict.keys():
            score = pn_dict[target_word]
            if is_nega_word(score):
                if target_word not in nega_word_list:
                    nega_word_list.append(target_word)

    return nega_word_list


def decorate(model, tagger, pn_dict, target_text, decorate_word_list, topn):
    '''
    decorate_word_listにある単語を使用して、ネガワードをポジワードに変換する
    '''
    nega_word_list = create_nega_word_list(tagger, target_text, pn_dict)

    naga_to_posi_dict, decorate_history_list = create_nega_to_posi_dict(
        model, nega_word_list, pn_dict, decorate_word_list, topn)

    # 変換語の結果用
    replace_text = target_text

    # 長い単語順にソート
    sorted_nega_word_list = sorted(naga_to_posi_dict.keys(), key=lambda nega_word: len(
        nega_word), reverse=True)

    # ネガワードをプレースホルダーで置き換え
    placeholder_dict = {}
    for n_word in sorted_nega_word_list:
        place_holder = util.generate_unique_place_holder(placeholder_dict)
        replace_text = replace_text.replace(n_word, place_holder)
        placeholder_dict[n_word] = place_holder

    # プレースホルダーをポジワードに置き換え、whitespace削除
    for n_word in sorted_nega_word_list:
        place_holder = placeholder_dict[n_word]
        replace_text = replace_text.replace(
            place_holder, naga_to_posi_dict[n_word])
        replace_text = replace_text.replace(' ', '')

    # チューニングのため、未変換のネガワード（ポジワードを見つけられなかったもの）を返す
    unreplaced_nega_word_list = util.diff_list(
        nega_word_list, naga_to_posi_dict.keys())

    return [target_text, replace_text, naga_to_posi_dict, unreplaced_nega_word_list, decorate_history_list]

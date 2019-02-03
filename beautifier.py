
import decorator
import util
import const


def decorate_with_logging(target_text_list, beautiful_word_list, topn):
    '''
    ループして美しくdecorateして結果をprint
    '''
    main_word = beautiful_word_list[0]

    print(f'{main_word}化開始...')
    print('')
    pn_dict = decorator.get_pn_dict1()
    model = util.load_model(const.WORD2VEC_MODEL_PATH)
    tagger = util.create_tagger()

    all_result = []
    for target_text in target_text_list:
        result = decorator.decorate(
            model, tagger, pn_dict, target_text, beautiful_word_list, topn)
        all_result.append(result)

    print(f'{main_word}化完了')
    print('')

    print('')
    print('***************')
    print('変更結果もれCheck')
    print('***************')
    not_decorated_list = [result[3]
                          for result in all_result if len(result[3]) != 0]
    if len(not_decorated_list) == 0:
        print(f'全て{main_word}化！')
    else:
        for not_decorated in not_decorated_list:
            print(not_decorated)

    print('')
    print('***************')
    print(f'使用{main_word}語チェック')
    print('***************')
    for beautiful_word in beautiful_word_list:
        print('')
        print('------------------')
        print(f'{beautiful_word}によって{main_word}化された単語')
        print('------------------')
        # あとで重複削除するためにsetに変換できるようtuple化
        res = [tuple(decorate_history) for result in all_result for decorate_history in result[4]
               if decorate_history[0] == beautiful_word]
        # 重複削除
        res = list(set(res))
        if len(res) == 0:
            print('なし！')
        else:
            for r in res:
                nega_word = r[1]
                posi_word = r[2]
                print(f'{nega_word} to {posi_word}')

    print('')
    print('***************')
    print('変更結果Check')
    print('***************')
    for result in all_result:
        print('-----------')
        print(result[0])
        print('↓')
        print(result[1])
        print('')


def beautify(target_text_list):
    beautiful_word_list = ['美', '聖', '愛', '慈愛', '涅槃']
    topn = 10
    decorate_with_logging(target_text_list, beautiful_word_list, topn)


def nirvanize(target_text_list):
    beautiful_word_list = ['涅槃', '慈悲', '浄土', '智慧']
    topn = 10
    decorate_with_logging(target_text_list, beautiful_word_list, topn)


def miyabinize(target_text_list):
    beautiful_word_list = ['雅', '京', '公家', '平安', '絵巻物']
    topn = 30
    decorate_with_logging(target_text_list, beautiful_word_list, topn)


if __name__ == "__main__":

    target_text_list = [
        'ハート マン軍曹',
        '話し掛けられた時以外口を開くな　口でクソたれる前と後に“サー”と言え　分かったか　蛆 虫ども',
        '貴様ら雌豚が　俺の訓練に生き残れたら　各人が兵器となる　戦争に祈りを捧げる死の司祭だ　その日までは蛆 虫だ！　地球上で最下等の生命体だ  貴様らは人間ではない　両生動物の糞をかき集めた値打ちしかない！',
        '貴様らは厳しい俺を嫌う　だが憎めば　それだけ学ぶ　俺は厳しいが公平だ　人種差別は許さん　黒豚　ユダ豚　イタ豚を　俺は見下さん　全て平等に価値がない！　俺の使命は役立たずを刈り取ることだ　愛する海兵隊の害虫を！　分かったか　蛆 虫！',
        '誰だ！　どの糞だ！　赤の手先のおフェラ豚め！',
        'ふざけるな！　大声だせ！　金玉を落としたか！',
        '糞 虫　名前は？',
        '糞餓鬼が！　貴様だろ　おく病魔羅は！',
        'パパの精液がシーツのシミになり　ママの割れ目に残った滓が　お前だ！　どこの穴で育った？ ',
    ]
    beautify(target_text_list)
    nirvanize(target_text_list)
    miyabinize(target_text_list)


    # target_text_list = ['誰だ！　どの糞だ！　赤の手先の　おフェラ豚め！']
    # # target_text_list = [
    # #     '戦争に祈りを捧げる死の司祭だ　その日まではウジ虫だ！'
    # # ]
    # beautiful_word_list = ['美', '涅槃']
    # topn = 10
    # decorate_with_logging(target_text_list, beautiful_word_list, topn)


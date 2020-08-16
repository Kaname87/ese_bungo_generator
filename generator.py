import argparse
import ese_bungo_generator
import similar_word_finder

def execute():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('action',
        type=str,
        choices=['update_word_list', 'update_csv', 'update_js', 'tmp'])
    parser.add_argument("-n", "--number", default=100, type=int)

    # for update_word_list
    parser.add_argument("--name-char-topn", default=7, type=int)
    parser.add_argument("--noun-topn", default=8, type=int)

    # 'update_csv', 'update_js'
    parser.add_argument("--no-update-list", action='store_true')

    # 'tmp'
    parser.add_argument("-w", "--word", default='', type=str)

    args = parser.parse_args()

    print('action: ' + args.action)
    print('number: ' + str(args.number))
    print('name_char_topn: ' + str(args.name_char_topn))
    print('noun_topn: ' + str(args.noun_topn))

    if args.action == 'update_word_list':
        # or not args.no_update_list:
        similar_word_finder.output_word_list(args.name_char_topn, args.noun_topn)

    if args.action == 'update_csv':
        # For twitter
        ese_bungo_generator.output_ese_bungo_to_csv(args.number)
    elif args.action == 'update_js':
        # For demosite
        ese_bungo_generator.output_ese_bungo_to_js(args.number)
    elif args.action == 'tmp':
        # For tmp generation
        if args.word == '':
            print('"word" is required')
            return

        word_dict = similar_word_finder.tmp(args.word)
        print(word_dict)
        result_list = ese_bungo_generator.tmp_replace_word(args.word, word_dict)
        print(result_list)
        print('Original')
        print(args.word)
        print('Replaced')
        for r in result_list:
            print('---')
            print(r)



    print('Done')

if __name__ == "__main__":
    execute()

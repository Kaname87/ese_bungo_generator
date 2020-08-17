# エセ文豪エセ名言ジェネレータ

実在する文豪の名言を元に、類似する名詞を置き換えることで存在しない文豪の存在しない名言を作り出します。

類似度の判定はWord2Vecで行なっており、モデルには東北大学 乾・岡崎研究室の[学習済みモデル](http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/)を使用しています。

## 実行順序
1. data/original_novel_list.jsonと同形式のファイル準備
2. similar_word_finder.py で類似語リスト生成
3. ese_bungo_generator.pyで元の文変。エセ名言生成

## requirements.txtについて
herokuにデプロイする関係で置いていますが、app.pyの実行に必要なものしか書かれていません。

生成用のファイルを動かすには
mecab-python3
gensim
が必要です。

# Web
## development
python -m web.app

# New demo
https://esebunko.vercel.app/
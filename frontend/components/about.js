import styles from './about.module.scss'

export default function About() {
    return (
        <section className={styles.about}>
            <h4>序文</h4>

            <p>文豪の作品の名文を元に自動生成されたテキスト集です。<br />
            文章中に使用された名詞に類似する名詞をランダムに置き換えることで文章を生成しています。</p>

            <p>単語の類似度の判定はWord2Vecを使用し、モデルには東北大学 乾・岡崎研究室の<a href="http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/" target="_blank" rel="noopener noreferrer">学習済みモデル</a>を使用しています。
            生成元の作品は全て<a href="https://www.aozora.gr.jp/index.html" target="_blank" rel="noopener noreferrer">青空文庫</a>からの引用です。</p>
        </section>
    )
}
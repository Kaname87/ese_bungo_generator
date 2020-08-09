import Head from 'next/head'
import Layout, { siteTitle } from '../components/layout'
import FakeQuoteCard from '../components/fakeQuoteCard'
import utilStyles from '../styles/utils.module.css'
import { getFakeQuote } from '../lib/api'


export default function Home({
  fakeQuote,
  fakeBook,
  fakeAuthor,
  quote,
  book,
  author,
}) {
  return (
    <Layout home>
      <>
      {/* <Head>
        <title>{siteTitle}</title>
      </Head> */}
      <section className={utilStyles.headingMd}>
        <FakeQuoteCard
          fakeQuote={fakeQuote}
          fakeBook={fakeBook}
          fakeAuthor={fakeAuthor}
          quote={quote}
          book={book}
          author={author}
        />
      </section>
      <section>
      {/* style="font-size: 0.8rem; margin: 30px 10%; padding-bottom: 30px; color:#7c4657; border:0.5px solid #7c4657;" */}
        <h4>序文</h4>
          文豪の作品の名文を元に生成された名文集です。<br />
          文章中に使用された名詞に類似する名詞をランダムに置き換えることで文章を生成しています。
          <br />
          <br />
        単語の類似度の判定はWord2Vecを使用し、モデルには東北大学 乾・岡崎研究室の<a href="http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/" target="_blank" rel="noopener noreferrer">学習済みモデル</a>を使用しています。
        生成元の作品は全て<a href="https://www.aozora.gr.jp/index.html" target="_blank" rel="noopener noreferrer">青空文庫</a>からの引用です。
      </section>
      </>
    </Layout>
  )
}

export async function getStaticProps() {
  const id = '2d12dcf4-3bae-418b-8005-aa550c76730c';
  const {
    fake_quote:fakeQuote,
    fake_book:fakeBook,
    fake_author:fakeAuthor,
    quote,
    book,
    author,
   } = await getFakeQuote(id)
  return {
    props: {
      fakeQuote,
      fakeBook,
      fakeAuthor,
      quote,
      book,
      author,
    }
  }
}

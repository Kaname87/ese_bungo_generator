import Layout from '../../components/layout';
import FakeQuoteCard from '../../components/fakeQuoteCard';

import { getFakeQuote, getFakeQuoteIdList } from '../../lib/api'
import { getIdPaths } from '../../lib/util'

export default function Quote({
  fakeQuote,
  fakeBook,
  fakeAuthor,
  quote,
  book,
  author,
}) {
  return (
    <Layout>
      <FakeQuoteCard
        fakeQuote={fakeQuote}
        fakeBook={fakeBook}
        fakeAuthor={fakeAuthor}
        quote={quote}
        book={book}
        author={author}
      />
    </Layout>
  )
}

export async function getStaticPaths() {
  return await getIdPaths(getFakeQuoteIdList)
}

export async function getStaticProps({ params }) {
  const {
    fake_quote:fakeQuote,
    fake_book:fakeBook,
    fake_author:fakeAuthor,
    quote,
    book,
    author,
   } = await getFakeQuote(params.id)
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

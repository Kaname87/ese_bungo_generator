import Layout from '../../components/layout';
import Link from "next/link"

import {
    getFakeAuthorListByAuthorId,
    getAuthorIdList,
} from '../../lib/api'

import { getIdPaths } from '../../lib/util'


export default function Author({

  fakeAuthorList,
  bookList,
  author,
}) {
  return (
    <Layout>

      <h1>{author.name}</h1>
      {bookList.map(book => {
          return (
            <div>
                <Link href="/books/[id]/quotes/[page]" as={`/books/${book.id}/quotes/1`}>
                    <a>{`『${book.title}』`}</a>
                </Link>
            </div>
          )
    })}
    <hr />
    {fakeAuthorList.map(fakeAuthor => (
        <div>
            <Link href="/fake_authors/[id]" as={`/fake_authors/${fakeAuthor.id}`}>
                <a>{fakeAuthor.name}</a>
            </Link>
            </div>
      ))}
    </Layout>
  )
}

export async function getStaticPaths() {
  return await getIdPaths(getAuthorIdList)
}

export async function getStaticProps({ params }) {

  const {
    author,
    book_list: bookList,
    fake_author_list: fakeAuthorList,
   } = await getFakeAuthorListByAuthorId(params.id)


  return {
    props: {
      author,
      bookList,
      fakeAuthorList,
    }
  }
}

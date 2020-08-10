import Link from "next/link"
import Layout from "../../../../../components/layout";
import Pager from "../../../../../components/pager"

import {
    getAuthorIdList,
    getFakeAuthorListByAuthorId,
 } from '../../../../../lib/api';
import { getAllChildrenPagePaths } from '../../../../../lib/util';

import { COUNT_PER_PAGE  }  from "../../../../../config/const";

export default function AuthorFakeAuthorList({
    author,
    bookList,
    fakeAuthorList, page, total, perPage }) {
  return (
    <Layout>
      <h1>エセ文豪一覧</h1>
      <p>{author.name}</p>
      {bookList.map((book) => <div
        key={book.id}
        className="post-teaser"
      >
        {/* <h2><Link href="/posts/[id]" as={`/posts/${post.slug}`}><a>{post.title}</a></Link></h2> */}
        <div>
        <Link href="/books/[id]/quotes/list/[page]" as={`/books/${book.id}/quotes/list/1`}><a>{book.title}</a></Link>
        </div>
      </div>)}

        <hr/>
        <hr/>

      {fakeAuthorList.map((fakeAuthor) => <div
        key={fakeAuthor.id}
        className="post-teaser"
      >
        {/* <h2><Link href="/posts/[id]" as={`/posts/${post.slug}`}><a>{post.title}</a></Link></h2> */}
        <div>
        <Link href="/fake_authors/[id]" as={`/fake_authors/${fakeAuthor.id}`}><a>{fakeAuthor.name}</a></Link>
        </div>
      </div>)}
      <Pager
        page={page} total={total} perPage={perPage}
        href="/authors/[id]/fake_authors/list/[page]"
        asCallback={(page) => `/authors/${author.id}/fake_authors/list/${page}`}
      />
    </Layout>
  )
}

/**
 * 有効な URL パラメータを全件返す
 */
export async function getStaticPaths() {
  return await getAllChildrenPagePaths(getAuthorIdList, getFakeAuthorListByAuthorId)
}

/**
 * ページコンポーネントで使用する値を用意する
 */
export async function getStaticProps({ params }) {
  const page = parseInt(params.page, 10)
  const offset = COUNT_PER_PAGE * (page-1)

  const {
        author,
        book_list: bookList,
        children_list: fakeAuthorList,
        children_total: total
   } = await getFakeAuthorListByAuthorId(params.id, offset, COUNT_PER_PAGE)


  return {
    props: {
      author,
      bookList,
      fakeAuthorList,
      page,
      total,
      perPage: COUNT_PER_PAGE,
    }
  }
}

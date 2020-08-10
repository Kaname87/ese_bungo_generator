import Link from "next/link"
import Layout from "../../../../../components/layout";
import Pager from "../../../../../components/pager"

import {
    getFakeAuthorIdList,
    getFakeBookListByFakeAuthorId,
 } from '../../../../../lib/api';
import { getAllChildrenPagePaths } from '../../../../../lib/util';

import { COUNT_PER_PAGE  }  from "../../../../../config/const";

export default function AuthorFakeBookList({
    fakeAuthor,
    fakeBookList,
    page, total, perPage }) {
  return (
    <Layout>
      <h1>エセ文豪作品一覧</h1>
      <p>{fakeAuthor.name}</p>
      {fakeBookList.map((fakeBook) => <div
        key={fakeBook.id}
        className="post-teaser"
      >
        {/* <h2><Link href="/posts/[id]" as={`/posts/${post.slug}`}><a>{post.title}</a></Link></h2> */}
        <div>
        <Link href="/fake_books/[id]/fake_quotes/list/[page]" as={`/fake_books/${fakeBook.id}/fake_quotes/list/1`}>
            <a>{fakeBook.title}</a></Link>
        </div>
      </div>)}

        <hr/>
        <hr/>
      <Pager
        page={page} total={total} perPage={perPage}
        href="/fake_authors/[id]/fake_books/list/[page]"
        asCallback={(page) => `/fake_authors/${fakeAuthor.id}/fake_books/list/${page}`}
      />
    </Layout>
  )
}


export async function getStaticPaths() {
  return await getAllChildrenPagePaths(
        getFakeAuthorIdList,
        getFakeBookListByFakeAuthorId
    )
}


export async function getStaticProps({ params }) {
  const page = parseInt(params.page, 10)
  const offset = COUNT_PER_PAGE * (page-1)

  const res = await getFakeBookListByFakeAuthorId(params.id, offset, COUNT_PER_PAGE)
//   console.log({res})
  const {
    fake_author: fakeAuthor,
    // book_list: bookList,
    children_list: fakeBookList,
    children_total: total
} = res


  return {
    props: {
      fakeAuthor,
      fakeBookList,
      page,
      total,
      perPage: COUNT_PER_PAGE,
    }
  }
}

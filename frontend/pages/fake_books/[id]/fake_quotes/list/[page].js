import Link from "next/link"
import Layout from "../../../../../components/layout"
import Pager from "../../../../../components/pager"


import { getFakeQuoteListByFakeBookId, getFakeBookIdList } from '../../../../../lib/api'
import {  getAllChildrenPagePaths } from '../../../../../lib/util'

import { COUNT_PER_PAGE  }  from "../../../../../config/const";
export default function FakeBookFakeQuoteList({
    fakeBook,
    fakeQuoteList, page, total, perPage }) {
  return (
    <Layout>
      <h1>エセ本の引用一覧</h1>
        {fakeBook.title}
      { fakeQuoteList.map(fakeQuote => <div
        key={fakeQuote.id}
        className="post-teaser"
      >
        {/* <h2><Link href="/posts/[id]" as={`/posts/${post.slug}`}><a>{post.title}</a></Link></h2> */}
        <div>
        {fakeQuote.id}
        <Link
            href="/fake_quotes/[id]"
            as={`/fake_quotes/${fakeQuote.id}`}>
            <a>{fakeQuote.text}</a>
        </Link>
        </div>
      </div>)}
      <Pager
        page={page} total={total} perPage={perPage}
        href="/fake_books/[id]/fake_quotes/list/[page]"
        asCallback={(page) => `/fake_books/${fakeBook.id}/fake_quotes/list/${page}`}
      />
    </Layout>
  )
}

export async function getStaticPaths() {
    return await getAllChildrenPagePaths(getFakeBookIdList, getFakeQuoteListByFakeBookId)
}

export async function getStaticProps({ params }) {
    const page = parseInt(params.page, 10)
    const offset = COUNT_PER_PAGE * (page-1)

    const {
        fake_book:fakeBook,
        children_list: fakeQuoteList,
        children_total:total,
     } = await getFakeQuoteListByFakeBookId(params.id, offset, COUNT_PER_PAGE)

    return {
      props: {
        fakeBook,
        fakeQuoteList,
        page,
        total,
        perPage: COUNT_PER_PAGE,
      }
    }
}

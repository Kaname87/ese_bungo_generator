import Link from "next/link"
import Layout from "../../../../../components/layout"
import Pager from "../../../../../components/pager"


import { getQuoteListByBookId, getBookIdList } from '../../../../../lib/api'
import {  getAllChildrenPagePaths } from '../../../../../lib/util'

import { COUNT_PER_PAGE  }  from "../../../../../config/const";
export default function BookQuoteList({ quoteList, page, total, perPage }) {
  return (
    <Layout>
      <h1>本の引用一覧</h1>

      { quoteList.map((quote) => <div
        key={quote.id}
        className="post-teaser"
      >
        {/* <h2><Link href="/posts/[id]" as={`/posts/${post.slug}`}><a>{post.title}</a></Link></h2> */}
        <div>
        {quote.id}
        <Link
            href="/quotes/[id]/fake_quotes/list/[page]"
            as={`/quotes/${quote.id}/fake_quotes/list/1`}>
            <a>!!!{quote.text}</a>
        </Link>
        </div>
      </div>)}
      <Pager
        page={page} total={total} perPage={perPage}
        href="/quotes/list/[page]"
        asCallback={(page) => `/quotes/list/${page}`}
      />
    </Layout>
  )
}

export async function getStaticPaths() {
    return await getAllChildrenPagePaths(getBookIdList, getQuoteListByBookId)
}

export async function getStaticProps({ params }) {
    const page = parseInt(params.page, 10)
    const offset = COUNT_PER_PAGE * (page-1)

    const {
        book,
        children_list: quoteList,
        children_total:total,
     } = await getQuoteListByBookId(params.id, offset, COUNT_PER_PAGE)

    return {
      props: {
        book,
        quoteList,
        page,
        total,
        perPage: COUNT_PER_PAGE,
      }
    }
}

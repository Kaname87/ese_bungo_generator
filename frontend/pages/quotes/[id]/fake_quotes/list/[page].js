import Link from "next/link"
import Layout from "../../../../../components/layout"
import Pager from "../../../../../components/pager"


import { getFakeQuoteListByQuoteId, getQuoteIdList } from '../../../../../lib/api'
import {  getAllChildrenPagePaths } from '../../../../../lib/util'

import { COUNT_PER_PAGE  }  from "../../../../../config/const";
export default function QuoteFakeQuoteList({ quote, fakeQuoteList, page, total, perPage }) {
  return (
    <Layout>
      <h1>エセ引用一覧</h1>

      { fakeQuoteList.map((fakeQuote) => <div
        key={fakeQuote.id}
        className="post-teaser"
      >
        {/* <h2><Link href="/posts/[id]" as={`/posts/${post.slug}`}><a>{post.title}</a></Link></h2> */}
        <div>
        <Link
            href="/fake_quotes/[id]"
            as={`/fake_quotes/${fakeQuote.id}`}>
            <a>{fakeQuote.text}</a>
        </Link>

        </div>
      </div>)}
      <Pager
        page={page} total={total} perPage={perPage}
        href="/quotes/[id]/fake_quotes/list/[page]"
        asCallback={(page) => `/quotes/${quote.id}/fake_quotes/list/${page}`}
      />
    </Layout>
  )
}

export async function getStaticPaths() {
    return await getAllChildrenPagePaths(getQuoteIdList, getFakeQuoteListByQuoteId)
}

export async function getStaticProps({ params }) {
    const page = parseInt(params.page, 10)
    const offset = COUNT_PER_PAGE * (page-1)

    const {
        quote,
        children_list: fakeQuoteList,
        children_total:total,
     } = await getFakeQuoteListByQuoteId(params.id, offset, COUNT_PER_PAGE)

    return {
      props: {
        quote,
        fakeQuoteList,
        page,
        total,
        perPage: COUNT_PER_PAGE,
      }
    }
}

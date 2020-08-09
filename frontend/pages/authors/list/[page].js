// import fs from "fs"
import Link from "next/link"
import Layout from "../../../components/layout";
import Pager from "../../../components/Pager"
// import { listContentFiles, readContentFiles } from "../../lib/content-loader"

import { getAuthorIdList, getAuthorList, recFetchIdList } from '../../../lib/api'

const COUNT_PER_PAGE = 2
export default function AuthorList({ authorList=[], page, total, perPage }) {
  return (
    <Layout>
      <h1>文豪一覧</h1>

      {authorList.map((author) => <div
        key={author.id}
        className="post-teaser"
      >
        {/* <h2><Link href="/posts/[id]" as={`/posts/${post.slug}`}><a>{post.title}</a></Link></h2> */}
        <div>
        <Link href="/authors/[id]" as={`/authors/${author.id}`}><a>{author.name}</a></Link>
        </div>
      </div>)}
      <Pager
        page={page} total={total} perPage={perPage}
        href="/authors/list/[page]"
        asCallback={(page) => `/authors/list/${page}`}
      />
    </Layout>
  )
}

/**
 * 有効な URL パラメータを全件返す
 */
export async function getStaticPaths() {
  const idList = await recFetchIdList(getAuthorIdList)
  // const fakeQuoteList = await recFetchIdList(getFakeQuoteIdList)
  // const posts = await listContentFiles({ fs })
  const pages = rangeArray(Math.ceil(idList.length / COUNT_PER_PAGE))
  const paths = pages.map((page) => ({
    params: { page: `${page}` }
  }))
  return {
    paths,
    fallback: false
  }
}

/**
 * ページコンポーネントで使用する値を用意する
 */
export async function getStaticProps({ params }) {
  const page = parseInt(params.page, 10)
  const offset = COUNT_PER_PAGE * (page-1)

  const {result_list: authorList, total } = await getAuthorList(offset, COUNT_PER_PAGE)


  console.log(authorList)

  return {
    props: {
      authorList,
      page,
      total,
      perPage: COUNT_PER_PAGE,
    }
  }
}

/**
 * ユーティリティ: 1 から指定された整数までを格納した Array を返す
 */
function rangeArray(length) {
  return Array.from({ length }, (_, i) => i + 1)
}
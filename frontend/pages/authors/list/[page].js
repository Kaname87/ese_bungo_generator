// import fs from "fs"
import Link from "next/link"
import Layout from "../../../components/layout";
import Pager from "../../../components/pager"
// import { listContentFiles, readContentFiles } from "../../lib/content-loader"

import { getAuthorIdList, getAuthorList } from '../../../lib/api'
import {  getPagePaths } from '../../../lib/util'
import { COUNT_PER_PAGE  }  from "../../../config/const";

export default function AuthorList({ authorList=[], page, total, perPage }) {
  return (
    <Layout>
      <h1>文豪一覧</h1>
test
      {authorList.map((author) => <div
        key={author.id}
        className="post-teaser"
      >
        {/* <h2><Link href="/posts/[id]" as={`/posts/${post.slug}`}><a>{post.title}</a></Link></h2> */}
        <div>
            <Link
                href="/authors/[id]/fake_authors/list/[page]"
                as={`/authors/${author.id}/fake_authors/list/1`}
            >
                <a>{author.name}</a>
            </Link>
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

export async function getStaticPaths() {
    return await getPagePaths(getAuthorIdList)
}

export async function getStaticProps({ params }) {
  const page = parseInt(params.page, 10)
  const offset = COUNT_PER_PAGE * (page-1)

  const {result_list: authorList, total } = await getAuthorList(offset, COUNT_PER_PAGE)

//   console.log(authorList)

  return {
    props: {
      authorList,
      page,
      total,
      perPage: COUNT_PER_PAGE,
    }
  }
}

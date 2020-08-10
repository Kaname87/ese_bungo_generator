// import fs from "fs"
import Link from "next/link"
import Layout from "../../../components/layout";
import Pager from "../../../components/pager"
// import { listContentFiles, readContentFiles } from "../../lib/content-loader"

import { getFakeAuthorIdList, getFakeAuthorList } from '../../../lib/api'
import {  getPagePaths } from '../../../lib/util'
import { COUNT_PER_PAGE  }  from "../../../config/const";

export default function FakeAuthorList({ fakeAuthorList, page, total, perPage }) {
  return (
    <Layout>
      <h1>エセ文豪一覧</h1>
test2
      {fakeAuthorList.map((fakeAuthor) => <div
        key={fakeAuthor.id}
        className="post-teaser"
      >
        {/* <h2><Link href="/posts/[id]" as={`/posts/${post.slug}`}><a>{post.title}</a></Link></h2> */}
        <div>
            <Link
                href="/fake_authors/[id]/fake_books/list/[page]"
                as={`/fake_authors/${fakeAuthor.id}/fake_books/list/1`}
            >
                <a>{fakeAuthor.name}</a>
            </Link>
        </div>
      </div>)}
      <Pager
        page={page} total={total} perPage={perPage}
        href="/fake_authors/list/[page]"
        asCallback={(page) => `/fake_authors/list/${page}`}
      />
    </Layout>
  )
}

export async function getStaticPaths() {
    return await getPagePaths(getFakeAuthorIdList)
}

export async function getStaticProps({ params }) {
  const page = parseInt(params.page, 10)
  const offset = COUNT_PER_PAGE * (page-1)

  const {result_list: fakeAuthorList, total } = await getFakeAuthorList(offset, COUNT_PER_PAGE)

//   console.log(fakeAuthorList)

  return {
    props: {
      fakeAuthorList,
      page,
      total,
      perPage: COUNT_PER_PAGE,
    }
  }
}

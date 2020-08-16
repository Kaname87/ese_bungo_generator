import Layout from "../../../../../components/layout";

import PagerWrapper from "../../../../../components/pagerWrapper";
import OriginalAuthor from "../../../../../components/originalAuthor";
import CommonAuthorList from "../../../../../components/commonAuthorList";
import {
  getAuthorIdList,
  getFakeAuthorListByAuthorId,
  getRandomFakeQuoteIdList,
} from "../../../../../lib/api";
import { getAllChildrenPagePaths } from "../../../../../lib/util";

import { COUNT_PER_PAGE } from "../../../../../config/const";

export default function AuthorFakeAuthorList({
  data: { author,fakeAuthorList, total, randomIdList },
  page,
  perPage,
}) {
  const pageTitle = `エセ文豪一覧 ${author.name}関連`;
  return (
    <Layout pageTitle={pageTitle} randomIdList={randomIdList}>
      <h1>{pageTitle}</h1>

      <PagerWrapper
        page={page}
        total={total}
        perPage={perPage}
        href="/authors/[id]/fake_authors/list/[page]"
        asCallback={(page) => `/authors/${author.id}/fake_authors/list/${page}`}
      >
        <CommonAuthorList targetAuthorList={fakeAuthorList} isFake />
      </PagerWrapper>
      <OriginalAuthor author={author} />
    </Layout>
  );
}

export async function getStaticPaths() {
  return await getAllChildrenPagePaths(
    getAuthorIdList,
    getFakeAuthorListByAuthorId
  );
}

export async function getStaticProps({ params }) {
  const page = parseInt(params.page, 10);
  const offset = COUNT_PER_PAGE * (page - 1);

  const {
    author,
    // book_list: bookList,
    children_list: fakeAuthorList,
    children_total: total,
  } = await getFakeAuthorListByAuthorId(params.id, offset, COUNT_PER_PAGE);
  const randomData = await getRandomFakeQuoteIdList();

  return {
    props: {
      data: {
        author,
        fakeAuthorList,
        total,
        randomIdList: randomData.id_list,
      },
      page,
      perPage: COUNT_PER_PAGE,
    },
  };
}

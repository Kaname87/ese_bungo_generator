import Layout from "../../../components/layout";
import CommonAuthorList from "../../../components/commonAuthorList";
import {
  getAuthorIdList,
  getAuthorList,
  getRandomFakeQuoteIdList,
} from "../../../lib/api";
import { getPagePaths } from "../../../lib/util";
import { COUNT_PER_PAGE_AUTHOR } from "../../../config/const";

import PagerWrapper from "../../../components/pagerWrapper";
export default function AuthorList({
  data: { authorList, total, randomIdList },
  page,
  perPage,
}) {
  const pageTitle = "文豪一覧";
  return (
    <Layout pageTitle={pageTitle} randomIdList={randomIdList}>
      <h1>{pageTitle}</h1>
      <PagerWrapper
        page={page}
        total={total}
        perPage={perPage}
        href="/authors/list/[page]"
        asCallback={(page) => `/authors/list/${page}`}
      >
        <CommonAuthorList targetAuthorList={authorList} />
      </PagerWrapper>
    </Layout>
  );
}

export async function getStaticPaths() {
  return await getPagePaths(getAuthorIdList, COUNT_PER_PAGE_AUTHOR);
}

export async function getStaticProps({ params }) {
  const page = parseInt(params.page, 10);
  const offset = COUNT_PER_PAGE_AUTHOR * (page - 1);

  const { authorList, total } = await getAuthorList(
    offset,
    COUNT_PER_PAGE_AUTHOR
  );

  const randomData = await getRandomFakeQuoteIdList();

  return {
    props: {
      data: {
        authorList,
        total,
        randomIdList: randomData.id_list,
      },
      page,
      perPage: COUNT_PER_PAGE_AUTHOR,
    },
  };
}

import Layout from "../../../components/layout";

import CommonAuthorList from "../../../components/commonAuthorList";

import PagerWrapper from "../../../components/pagerWrapper";
import {
  getFakeAuthorIdList,
  getFakeAuthorList,
  getRandomFakeQuoteIdList,
} from "../../../lib/api";
import { getPagePaths } from "../../../lib/util";
import { COUNT_PER_PAGE_AUTHOR } from "../../../config/const";

export default function FakeAuthorList({
  data: { fakeAuthorList, total, randomIdList },
  page,
  perPage,
}) {
  const pageTitle = "エセ文豪一覧";
  return (
    <Layout pageTitle={pageTitle} randomIdList={randomIdList}>
      <h1>{pageTitle}</h1>
      <PagerWrapper
        page={page}
        total={total}
        perPage={perPage}
        href="/fake_authors/list/[page]"
        asCallback={(page) => `/fake_authors/list/${page}`}
      >
        <CommonAuthorList targetAuthorList={fakeAuthorList} isFake />
      </PagerWrapper>
    </Layout>
  );
}

export async function getStaticPaths() {
  return await getPagePaths(getFakeAuthorIdList, COUNT_PER_PAGE_AUTHOR);
}

export async function getStaticProps({ params }) {
  const page = parseInt(params.page, 10);
  const offset = COUNT_PER_PAGE_AUTHOR * (page - 1);

  const { result_list: fakeAuthorList, total } = await getFakeAuthorList(
    offset,
    COUNT_PER_PAGE_AUTHOR
  );

  const randomData = await getRandomFakeQuoteIdList();
  //   console.log(fakeAuthorList)

  return {
    props: {
      data: {
        fakeAuthorList,
        randomIdList: randomData.id_list,
        total,
      },
      page,
      perPage: COUNT_PER_PAGE_AUTHOR,
    },
  };
}

import Layout from '../../../components/layout';

import CommonQuoteList from '../../../components/commonQuoteList';
import PagerWrapper from '../../../components/pagerWrapper';
import {
  getFakeQuoteIdList,
  getFakeQuoteList,
  getRandomFakeQuoteIdList,
} from '../../../lib/api';
import { getPagePaths } from '../../../lib/util';
import { COUNT_PER_PAGE } from '../../../config/const';

export default function FakeQuoteListPage({
  data: { resultList, total, randomIdList },
  page,
  perPage,
}) {
  const pageTitle = 'エセ引用一覧';
  return (
    <Layout pageTitle={pageTitle} randomIdList={randomIdList}>
      <h1>{pageTitle}</h1>
      <PagerWrapper
        page={page}
        total={total}
        perPage={perPage}
        href='/fake_quotes/list/[page]'
        asCallback={(page) => `/fake_quotes/list/${page}`}
      >
        <CommonQuoteList targetQuoteList={resultList} isFake />
      </PagerWrapper>
    </Layout>
  );
}

export async function getStaticPaths() {
  return await getPagePaths(getFakeQuoteIdList, COUNT_PER_PAGE);
}

export async function getStaticProps({ params }) {
  const page = parseInt(params.page, 10);
  const offset = COUNT_PER_PAGE * (page - 1);

  const { result_list: resultList, total } = await getFakeQuoteList(
    offset,
    COUNT_PER_PAGE
  );

  const randomData = await getRandomFakeQuoteIdList();

  return {
    props: {
      data: {
        resultList,
        randomIdList: randomData.id_list,
        total,
      },
      page,
      perPage: COUNT_PER_PAGE,
    },
  };
}

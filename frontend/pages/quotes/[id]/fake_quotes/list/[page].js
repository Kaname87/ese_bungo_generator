import Layout from '../../../../../components/layout';
import PagerWrapper from '../../../../../components/pagerWrapper';
import {
  getFakeQuoteListByQuoteId,
  getQuoteIdList,
  getRandomFakeQuoteIdList,
} from '../../../../../lib/api';
import { getAllChildrenPagePaths } from '../../../../../lib/util';

import { COUNT_PER_PAGE } from '../../../../../config/const';
import CommonQuoteList from '../../../../../components/commonQuoteList';
import OriginalQuote from '../../../../../components/originalQuote';
export default function QuoteFakeQuoteList({
  data: {
    quote,
    fakeQuoteList,
    total,
    randomIdList,
},
  page,
  perPage,
}) {
  const pageTitle = `${quote.text}関連 エセ引用一覧`
  return (
    <Layout pageTitle={pageTitle} randomIdList={randomIdList}>
      <h1>エセ引用一覧</h1>
      <OriginalQuote quote={quote}/>
      <PagerWrapper
        page={page}
        total={total}
        perPage={perPage}
        href='/quotes/[id]/fake_quotes/list/[page]'
        asCallback={(page) => `/quotes/${quote.id}/fake_quotes/list/${page}`}
      >
        <CommonQuoteList targetQuoteList={fakeQuoteList} isFake />

      </PagerWrapper>
    </Layout>
  );
}

export async function getStaticPaths() {
  return await getAllChildrenPagePaths(
    getQuoteIdList,
    getFakeQuoteListByQuoteId
  );
}

export async function getStaticProps({ params }) {
  const page = parseInt(params.page, 10);
  const offset = COUNT_PER_PAGE * (page - 1);

  const {
    // author,
    // book,
    quote,
    children_list: fakeQuoteList,
    children_total: total,
  } = await getFakeQuoteListByQuoteId(params.id, offset, COUNT_PER_PAGE);
  const randomData = await getRandomFakeQuoteIdList()

  return {
    props: {
      data: {
        quote,
        fakeQuoteList,
        total,
        randomIdList:randomData.id_list,
      },
      page,
      perPage: COUNT_PER_PAGE,
    },
  };
}

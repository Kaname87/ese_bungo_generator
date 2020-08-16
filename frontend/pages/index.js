import Layout from "../components/layout";
import FakeQuoteCard from "../components/fakeQuoteCard";

import { getFakeQuote, getRandomFakeQuoteIdList } from "../lib/api";

import About from "../components/about";
import { TOP_PAGE_FAKE_QUOTE_ID } from "../config/const";

export default function Home({ data }) {
  return (
    <Layout pageTitle="表紙" randomIdList={data.randomIdList}>

      <FakeQuoteCard fakeQuoteData={data} />
      <About />

    </Layout>
  );
}

export async function getStaticProps() {
  const fkQuoteData = await getFakeQuote(TOP_PAGE_FAKE_QUOTE_ID);
  const randomData = await getRandomFakeQuoteIdList(TOP_PAGE_FAKE_QUOTE_ID);
  const data = {
    ...fkQuoteData,
    randomIdList: randomData.id_list,
  };

  return {
    props: {
      data,
    },
  };
}

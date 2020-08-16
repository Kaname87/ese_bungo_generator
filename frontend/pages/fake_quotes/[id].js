import Layout from '../../components/layout';
import FakeQuoteCard from '../../components/fakeQuoteCard';

import {
  getFakeQuote,
  getFakeQuoteIdList,
  getRandomFakeQuoteIdList,
} from '../../lib/api'
import { getIdPaths } from '../../lib/util'

export default function FakeQuote({
  data: {
    fakeQuoteData,
    randomIdList,
  }
}) {

  return (
    // Check if this affect to pageload
    <Layout pageTitle={fakeQuoteData.fakeQuote.text} randomIdList={randomIdList}>
      <FakeQuoteCard
        fakeQuoteData={fakeQuoteData}
      />
    </Layout>
  )
}

export async function getStaticPaths() {
  return await getIdPaths(getFakeQuoteIdList)
}

export async function getStaticProps({ params }) {
  const fkQuoteData = await getFakeQuote(params.id)
  const randomData = await getRandomFakeQuoteIdList(params.id)
  const randomIdList = randomData.id_list
  const fakeQuoteData = {
    ...fkQuoteData,
    randomIdList,
  }

  return {
    props: {
      data:{
        fakeQuoteData,
        randomIdList,
      }
    }
  }
}
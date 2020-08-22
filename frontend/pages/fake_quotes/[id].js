import Layout from "../../components/layout";
import FakeQuoteCard from "../../components/fakeQuoteCard";
import TwitterIcon from "../../components/twitterIcon";
import {
  getFakeQuote,
  getFakeQuoteIdList,
  getRandomFakeQuoteIdList,
} from "../../lib/api";
import { getIdPaths } from "../../lib/util";

export default function FakeQuote({ data: { fakeQuoteData, randomIdList } }) {
  const {
    author,
    book,
    quote,
    fakeAuthor,
    fakeBook,
    fakeQuote,
  } = fakeQuoteData;

  const ogpOptions = {
    author: author.name,
    book: book.title,
    quote: quote.text,
    fakeAuthor:fakeAuthor.name,
    fakeBook: fakeBook.title,
    fakeQuote: fakeQuote.text,
  };

  var ogpQueryString = Object.keys(ogpOptions)
    .map((key) => {
      return encodeURIComponent(key) + "=" + encodeURIComponent(ogpOptions[key]);
    })
    .join("&");
  return (
    // Check if this affect to pageload
    <Layout
      pageTitle={fakeQuoteData.fakeQuote.text}
      randomIdList={randomIdList}
      ogpQueryString={ogpQueryString}
    >
      <FakeQuoteCard fakeQuoteData={fakeQuoteData} />
      <TwitterIcon
        fakeAuthor={fakeAuthor}
        fakeBook={fakeBook}
        fakeQuote={fakeQuote}
      />
    </Layout>
  );
}

export async function getStaticPaths() {
  return await getIdPaths(getFakeQuoteIdList);
}

export async function getStaticProps({ params }) {
  const fkQuoteData = await getFakeQuote(params.id);
  const randomData = await getRandomFakeQuoteIdList(params.id);
  const randomIdList = randomData.id_list;
  const fakeQuoteData = {
    ...fkQuoteData,
    randomIdList,
  };

  return {
    props: {
      data: {
        fakeQuoteData,
        randomIdList,
      },
    },
  };
}

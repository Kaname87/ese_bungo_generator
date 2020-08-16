import Layout from '../components/layout';
import FakeQuoteCard from '../components/fakeQuoteCard';
import { NOT_FOUND_DATA } from '../config/const';

export default function NotFoundPage({ data }) {
  const pageTitle = '404';
  return (
    <Layout pageTitle={pageTitle}>
      <h1>{pageTitle}</h1>
      <FakeQuoteCard fakeQuoteData={data} isError />
    </Layout>
  );
}

export async function getStaticProps() {
  return {
    props: {
      data: NOT_FOUND_DATA,
    },
  };
}

import Layout from "../../../../../components/layout";

import PagerWrapper from "../../../../../components/pagerWrapper";
import FakeAuthor from "../../../../../components/fakeAuthor";
import CommonBookList from "../../../../../components/commonBookList";
import {
  getAuthorIdList,
  getBookListByAuthorId,
  getRandomFakeQuoteIdList,
} from "../../../../../lib/api";
import { getAllChildrenPagePaths } from "../../../../../lib/util";

import { COUNT_PER_PAGE } from "../../../../../config/const";

export default function AuthorBookList({
  data: { author, bookList, total, randomIdList },
  page,
  perPage,
}) {
  const pageTitle = author.name;
  return (
    <Layout pageTitle={pageTitle} randomIdList={randomIdList}>
      <h1>{pageTitle}</h1>
      <PagerWrapper
        page={page}
        total={total}
        perPage={perPage}
        href="/authors/[id]/books/list/[page]"
        asCallback={(page) => `/authors/${author.id}/books/list/${page}`}
      >
        <h4>著作</h4>
        <CommonBookList targetBookList={bookList} />
      </PagerWrapper>

      <FakeAuthor author={author} />
    </Layout>
  );
}

export async function getStaticPaths() {
  return await getAllChildrenPagePaths(getAuthorIdList, getBookListByAuthorId);
}

export async function getStaticProps({ params }) {
  const page = parseInt(params.page, 10);
  const offset = COUNT_PER_PAGE * (page - 1);

  const {
    author,
    children_list: bookList,
    children_total: total,
  } = await getBookListByAuthorId(params.id, offset, COUNT_PER_PAGE);
  const randomData = await getRandomFakeQuoteIdList();

  return {
    props: {
      data: {
        author,
        bookList,
        total,
        randomIdList: randomData.id_list,
      },
      page,
      perPage: COUNT_PER_PAGE,
    },
  };
}

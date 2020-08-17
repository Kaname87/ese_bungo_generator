import Layout from "../../../../../components/layout";

import CommonBookList from "../../../../../components/commonBookList";

import PagerWrapper from "../../../../../components/pagerWrapper";
import {
  getFakeAuthorIdList,
  getFakeBookListByFakeAuthorId,
  getRandomFakeQuoteIdList,
} from "../../../../../lib/api";
import { getAllChildrenPagePaths } from "../../../../../lib/util";
import OriginalAuthor from "../../../../../components/originalAuthor";
import { COUNT_PER_PAGE } from "../../../../../config/const";

export default function AuthorFakeBookList({
  data: {
    author,
    //  bookList,
    fakeAuthor,
    fakeBookList,
    total,
    randomIdList,
  },
  page,
  perPage,
}) {
  const pageTitle = fakeAuthor.name;
  return (
    <Layout pageTitle={pageTitle} randomIdList={randomIdList}>
      <h1>{pageTitle}</h1>
      <OriginalAuthor author={author} />
      <PagerWrapper
        page={page}
        total={total}
        perPage={perPage}
        href="/fake_authors/[id]/fake_books/list/[page]"
        asCallback={(page) =>
          `/fake_authors/${fakeAuthor.id}/fake_books/list/${page}`
        }
      >
        <h4>著作</h4>
        <CommonBookList targetBookList={fakeBookList} isFake />
      </PagerWrapper>
    </Layout>
  );
}

export async function getStaticPaths() {
  return await getAllChildrenPagePaths(
    getFakeAuthorIdList,
    getFakeBookListByFakeAuthorId
  );
}

export async function getStaticProps({ params }) {
  const page = parseInt(params.page, 10);
  const offset = COUNT_PER_PAGE * (page - 1);

  const {
    author,
    book_list: bookList,
    fake_author: fakeAuthor,
    children_list: fakeBookList,
    children_total: total,
  } = await getFakeBookListByFakeAuthorId(params.id, offset, COUNT_PER_PAGE);

  const randomData = await getRandomFakeQuoteIdList();
  return {
    props: {
      data: {
        author,
        bookList,
        fakeAuthor,
        fakeBookList,
        total,
        randomIdList: randomData.id_list,
      },
      page,
      perPage: COUNT_PER_PAGE,
    },
  };
}

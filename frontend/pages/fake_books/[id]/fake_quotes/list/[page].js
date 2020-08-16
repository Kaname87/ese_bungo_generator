import Link from "next/link";
import Layout from "../../../../../components/layout";

import PagerWrapper from "../../../../../components/pagerWrapper";
import CommonQuoteList from "../../../../../components/commonQuoteList";
import OriginalBook from "../../../../../components/originalBook";
import {
  getFakeQuoteListByFakeBookId,
  getFakeBookIdList,
  getRandomFakeQuoteIdList,
} from "../../../../../lib/api";
import { getAllChildrenPagePaths } from "../../../../../lib/util";

import { COUNT_PER_PAGE } from "../../../../../config/const";
export default function FakeBookFakeQuoteList({
  data: {
    // author,
    book,
    fakeAuthor,
    fakeBook,
    fakeQuoteList,
    randomIdList,
    total,
  },
  page,
  perPage,
}) {
  const pageTitle = `『${fakeBook.title}』`;
  return (
    <Layout pageTitle={pageTitle} randomIdList={randomIdList}>
      <h1>{pageTitle}</h1>
      <OriginalBook book={book} />
      <p>
        <Link
          href="/fake_authors/[id]/fake_books/list/[page]"
          as={`/fake_authors/${fakeAuthor.id}/fake_books/list/1`}
        >
          <a>{fakeAuthor.name}</a>
        </Link>
        {` 著`}
      </p>
      <PagerWrapper
        page={page}
        total={total}
        perPage={perPage}
        href="/fake_books/[id]/fake_quotes/list/[page]"
        asCallback={(page) =>
          `/fake_books/${fakeBook.id}/fake_quotes/list/${page}`
        }
      >
        <h4>引用</h4>
        <CommonQuoteList targetQuoteList={fakeQuoteList} isFake />
      </PagerWrapper>
    </Layout>
  );
}

export async function getStaticPaths() {
  return await getAllChildrenPagePaths(
    getFakeBookIdList,
    getFakeQuoteListByFakeBookId
  );
}

export async function getStaticProps({ params }) {
  const page = parseInt(params.page, 10);
  const offset = COUNT_PER_PAGE * (page - 1);

  const {
    // author,
    book,
    fake_author: fakeAuthor,
    fake_book: fakeBook,
    children_list: fakeQuoteList,
    children_total: total,
  } = await getFakeQuoteListByFakeBookId(params.id, offset, COUNT_PER_PAGE);

  const randomData = await getRandomFakeQuoteIdList();
  return {
    props: {
      data: {
        // author,
        book,
        fakeAuthor,
        fakeBook,
        fakeQuoteList,
        total,
        randomIdList: randomData.id_list,
      },
      page,
      perPage: COUNT_PER_PAGE,
    },
  };
}

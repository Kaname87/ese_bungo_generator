import Layout from "../../../../../components/layout";
import PagerWrapper from "../../../../../components/pagerWrapper";
import Link from "next/link";
import {
  getQuoteListByBookId,
  getBookIdList,
  getRandomFakeQuoteIdList,
} from "../../../../../lib/api";
import { getAllChildrenPagePaths } from "../../../../../lib/util";

import { COUNT_PER_PAGE } from "../../../../../config/const";

import CommonQuoteList from "../../../../../components/commonQuoteList";

import AozoraInfo from "../../../../../components/aozoraInfo";

export default function BookQuoteList({
  data: { author, book, quoteList, total, randomIdList },
  page,
  perPage,
}) {
  const pageTitle = `『${book.title}』`;
  return (
    <Layout pageTitle={pageTitle} randomIdList={randomIdList}>
      <h1>{pageTitle}</h1>
      <p>
        <Link
          href="/authors/[id]/fake_authors/list/[page]"
          as={`/authors/${author.id}/fake_authors/list/1`}
        >
          <a>{author.name}</a>
        </Link>
        {` 著`}
      </p>

      <PagerWrapper
        page={page}
        total={total}
        perPage={perPage}
        href="/quotes/list/[page]"
        asCallback={(page) => `/quotes/list/${page}`}
      >
        <h4>引用</h4>
        <CommonQuoteList targetQuoteList={quoteList} />
      </PagerWrapper>
      <AozoraInfo book={book} />
    </Layout>
  );
}

export async function getStaticPaths() {
  return await getAllChildrenPagePaths(getBookIdList, getQuoteListByBookId);
}

export async function getStaticProps({ params }) {
  const page = parseInt(params.page, 10);
  const offset = COUNT_PER_PAGE * (page - 1);

  const {
    author,
    book,
    children_list: quoteList,
    children_total: total,
  } = await getQuoteListByBookId(params.id, offset, COUNT_PER_PAGE);
  const randomData = await getRandomFakeQuoteIdList();

  return {
    props: {
      data: {
        author,
        book,
        quoteList,
        total,
        randomIdList: randomData.id_list,
      },
      page,
      perPage: COUNT_PER_PAGE,
    },
  };
}

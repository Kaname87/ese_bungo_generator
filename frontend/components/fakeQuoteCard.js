import styles from "./fakeQuoteCard.module.scss";

import Profile from "./profile";
import Link from "next/link";
import { useState, useEffect } from "react";

import RandomButton from "./randomButton";
import { useRouter } from "next/router";

import TwitterIcon from "./twitterIcon";

const fakeQuotePath = "/fake_quotes/[id]";

export default function fakeQuoteCard({ fakeQuoteData, isError = false }) {
  const router = useRouter();
  const [data, setData] = useState(fakeQuoteData);

  useEffect(() => {
    if (data.fakeQuote.id !== fakeQuoteData.fakeQuote.id) {
      setData(fakeQuoteData);
    }
  }, [fakeQuoteData.fakeQuote.id]);

  const {
    fakeQuote,
    fakeBook,
    fakeAuthor,
    quote,
    book,
    author,
    randomIdList = [],
  } = data;

  return (
    <section>
      <div className={styles.fake}>
        <div className={styles.fakeAuthorWrapper}>
          <RandomButton idList={randomIdList} />

          <div className={styles.fakeAuthor} id="fake_author_profile">
            <Profile alt="エセ文豪著者近影" profileIdx={isError ? 1 : 0} />
          </div>

          <RandomButton idList={randomIdList} />
        </div>

        <div className={styles.novel}>
          <p className={styles.fakeQuote}>{fakeQuote.text}</p>
          <p className={styles.fakeCite}>
            <span>
              {isError ? (
                <span className={styles.fakeAuthorName}>{fakeAuthor.name}</span>
              ) : (
                <Link
                  href="/fake_authors/[id]/fake_books/list/[page]"
                  as={`/fake_authors/${fakeAuthor.id}/fake_books/list/1`}
                >
                  <a className={styles.fakeAuthorName}>{fakeAuthor.name}</a>
                </Link>
              )}
              {isError ? (
                <span>{`『${fakeBook.title}』`}</span>
              ) : (
                <Link
                  href="/fake_books/[id]/fake_quotes/list/[page]"
                  as={`/fake_books/${fakeBook.id}/fake_quotes/list/1`}
                >
                  <a>{`『${fakeBook.title}』`}</a>
                </Link>
              )}
            </span>
          </p>
        </div>
      </div>
      <div className={styles.originalInfo}>
        <blockquote>
          {isError ? (
            <span className={styles.originalQuote}>{quote.text}</span>
          ) : (
            <Link
              href="/quotes/[id]/fake_quotes/list/[page]"
              as={`/quotes/${quote.id}/fake_quotes/list/1`}
            >
              <a className={styles.originalQuote}>{quote.text}</a>
            </Link>
          )}

          <cite className={styles.originalCite}>
            {isError ? (
              <span>{author.name}</span>
            ) : (
              <Link
                href="/authors/[id]/books/list/[page]"
                as={`/authors/${author.id}/books/list/1`}
              >
                <a>{author.name}</a>
              </Link>
            )}
            {isError ? (
              <span>{`『${book.title}』`}</span>
            ) : (
              <Link
                href="/books/[id]/quotes/list/[page]"
                as={`/books/${book.id}/quotes/list/1`}
              >
                <a>{`『${book.title}』`}</a>
              </Link>
            )}
          </cite>
        </blockquote>
      </div>
      <TwitterIcon
        fakeAuthor={fakeAuthor}
        fakeBook={fakeBook}
        fakeQuote={fakeQuote}
      />
    </section>
  );
}

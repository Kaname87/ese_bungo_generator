import Link from "next/link";
import styles from "./commonAuthorList.module.scss";
import { CHILDREN_MAX_DISPLAY } from "../config/const";

export default function CommonAuthorList({ targetAuthorList, isFake = false }) {
  const child_key = isFake ? "fake_book" : "book";
  const getAuthorLinkInfo = (isFake, id) =>
    isFake
      ? {
          href: "/fake_authors/[id]/fake_books/list/[page]",
          as: `/fake_authors/${id}/fake_books/list/1`,
        }
      : {
          href: "/authors/[id]/books/list/[page]",
          as: `/authors/${id}/books/list/1`,
        };

  const getAuthorLinkbyId = (isFake, id, name) => {
    const { href, as } = getAuthorLinkInfo(isFake, id);
    return (
      <Link href={href} as={as}>
        <a>{name}</a>
      </Link>
    );
  };

  const getBookLinkInfo = (isFake, id) =>
    isFake
      ? {
          href: "/fake_books/[id]/fake_quotes/list/[page]",
          as: `/fake_books/${id}/fake_quotes/list/1`,
        }
      : {
          href: "/books/[id]/quotes/list/[page]",
          as: `/books/${id}/quotes/list/1`,
        };
  const getBookLinkbyId = (isFake, id, title) => {
    const { href, as } = getBookLinkInfo(isFake, id);
    return (
      <Link href={href} as={as}>
        <a>{`『${title}』`}</a>
      </Link>
    );
  };

  return (
    <div className={styles.targetList}>
      {targetAuthorList.map((author) => (
        <div key={author.id} className={styles.targetBook}>
          <p className={styles.author}>
            {getAuthorLinkbyId(isFake, author.id, author.name)}
          </p>

          <ul>
            {author[`${child_key}_list`] &&
              author[`${child_key}_list`].map((book) => (
                <li key={book.id}>
                  {getBookLinkbyId(isFake, book.id, book.title)}
                </li>
              ))}
            {author[`${child_key}_total`] > CHILDREN_MAX_DISPLAY && (
              <li className={styles.more}>他</li>
            )}
          </ul>
        </div>
      ))}
    </div>
  );
}

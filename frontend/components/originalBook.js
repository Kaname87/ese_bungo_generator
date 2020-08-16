import Link from "next/link";

import styles from "./originalAuthor.module.scss";
import RelatedInfo from "./relatedInfo";

export default function OriginalBook({ book }) {
  return (
    <RelatedInfo>
      <p className={styles.author}>
        <Link
          href="/books/[id]/quotes/list/[page]"
          as={`/books/${book.id}/quotes/list/1`}
        >
        <a>{`『${book.title}』`}</a>
        </Link>
      </p>
    </RelatedInfo>
  );
}

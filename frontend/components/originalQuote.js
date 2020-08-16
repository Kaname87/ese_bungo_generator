import Link from "next/link";

import styles from "./originalAuthor.module.scss";
import RelatedInfo from "./relatedInfo";

export default function OriginalQuote({ quote }) {

  return (
    <RelatedInfo>
      <p className={styles.author}>
        <Link
          href="/quotes/[id]/fake_quotes/list/[page]"
          as={`/quotes/${quote.id}/fake_quotes/list/1`}
        >
        <a>{quote.text}</a>
        </Link>
      </p>
    </RelatedInfo>
  );
}

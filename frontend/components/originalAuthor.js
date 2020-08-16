import Link from "next/link";

import styles from "./originalAuthor.module.scss";
import RelatedInfo from "./relatedInfo";

export default function OriginaAuthor({ author }) {
  return (

    <RelatedInfo>
      <p className={styles.author}>
        <Link
          href="/authors/[id]/books/list/[page]"
          as={`/authors/${author.id}/books/list/1`}
        >
          <a>{author.name}</a>
        </Link>
      </p>
    </RelatedInfo>
  );
}

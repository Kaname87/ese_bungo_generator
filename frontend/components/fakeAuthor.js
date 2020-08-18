import Link from 'next/link';

import styles from './fakeAuthor.module.scss';
import RelatedInfo from './relatedInfo'

export default function FakeAuthor({
  author
}) {
  return (
    <RelatedInfo hideLineBottom>
      {author && (
      <p className={styles.author}>
        <Link
          href='/authors/[id]/fake_authors/list/[page]'
          as={`/authors/${author.id}/fake_authors/list/1`}
        >
          <a>派生文豪一覧</a>
        </Link>
      </p>
    )}
    </RelatedInfo>
  );
}

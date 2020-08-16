import Link from "next/link";
import styles from "./pager.module.scss";
const Pager = (props) => {
  const { total, page, perPage, href, asCallback } = props;

  const prevPage = page > 1 ? page - 1 : -1;

  const lastPage = Math.ceil(total / perPage);

  if (lastPage == 1) {
    return null;
  }

  const isFirstPage = page === 1;
  const isLastPage = page === lastPage;

  let nextPage = Number.MAX_SAFE_INTEGER;
  if (page < lastPage) {
    nextPage = page + 1;
  }

  const renderPagerItem = (href, page) => (
    <span className={styles.pagerItem}>
      <Link href={href} as={asCallback(page)}>
        <a>{page}</a>
      </Link>
    </span>
  );
  if (total == 1) {
    null;
  }

  return (
    <div className={styles.pager}>
      <span className={styles.pagerItem}>
        {!isFirstPage ? (
          <Link href={href} as={asCallback(1)}>
            <a>«</a>
          </Link>
        ) : (
          `«`
        )}
      </span>

      {prevPage - 2 > 0 && <span className={styles.pagerItem}>...</span>}

      {prevPage - 1 > 0 && renderPagerItem(href, prevPage - 1)}

      {prevPage > 0 && renderPagerItem(href, prevPage)}

      <span className={styles.pagerItem}>{page}</span>

      {nextPage <= lastPage && renderPagerItem(href, nextPage)}

      {nextPage + 1 <= lastPage && renderPagerItem(href, nextPage + 1)}

      {nextPage + 2 <= lastPage && (
        <span className={styles.pagerItem}>...</span>
      )}

      <span className={styles.pagerItem}>
        {!isLastPage ? (
          <Link href={href} as={asCallback(lastPage)}>
            <a>»</a>
          </Link>
        ) : (
          `»`
        )}
      </span>
    </div>
  );
};
export default Pager;

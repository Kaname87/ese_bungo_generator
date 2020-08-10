import Link from "next/link"
const Pager = (props) => {
  const { total, page, perPage, href, asCallback } = props

  const prevPage = page > 1 ? page - 1 : -1;

  const lastPage = Math.ceil(total / perPage)

  if (lastPage == 1) {
      return (<></>)
  }

  const isFirstPage = page === 1;
  const isLastPage = page === lastPage;

  let nextPage = Number.MAX_SAFE_INTEGER
  if (page < lastPage) {
    nextPage = page + 1
  }


  return (
    <div className="pager">
        <span className="pager-item">
            {!isFirstPage ? (
                <Link href={href} as={asCallback(1)}>
                    <a>«</a>
                </Link>
                ) : `«`}
        </span>

        <span className="pager-item">
            {(prevPage-1) > 0 ? (
            <Link href={href} as={asCallback(prevPage-1)}>
                <a>{prevPage-1}</a>
            </Link>
            ) : ``}
        </span>

        <span className="pager-item">
            {prevPage > 0 ? (
            <Link href={href} as={asCallback(prevPage)}>
                <a>{prevPage}</a>
            </Link>
            ) : ``}
        </span>

        <span className="pager-item">{page}</span>

        <span className="pager-item">
            {nextPage <= lastPage ? (
            <Link href={href} as={asCallback(nextPage)}>
                <a>{nextPage}</a>
            </Link>
            ) : ``}
        </span>

        <span className="pager-item">
            {nextPage +1 <= lastPage ? (
            <Link href={href} as={asCallback(nextPage +1)}>
                <a>{nextPage +1}</a>
            </Link>
            ) : ``}
        </span>

        <span className="pager-item">
            {!isLastPage ? (
            <Link href={href} as={asCallback(lastPage)}>
                <a>»</a>
            </Link>
            ) : `»`}
        </span>

      <style jsx>{`
        .pager {
          display: flex;
          flex-direction: row;
          justify-content: center;
          flew-wrap: nowrap;
        }
        .pager-item {
          margin: 0 1em;
        }
      `}</style>
    </div>
  )
}
export default Pager
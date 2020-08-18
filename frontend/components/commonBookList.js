import Link from 'next/link';
import styles from './commonBookList.module.scss'
export default function CommonBookList({ targetBookList, isFake=false }) {

  const getBookLinkInfo = (isFake, id) => (
    isFake ?
    {
      href:'/fake_books/[id]/fake_quotes/list/[page]',
      as:`/fake_books/${id}/fake_quotes/list/1`,
    } :
    {
      href:'/books/[id]/quotes/list/[page]',
      as:`/books/${id}/quotes/list/1`,
    }
  )
  const getBookLinkbyId = (isFake, id, title) => {
    const { href, as } = getBookLinkInfo(isFake, id)
    return (
      <Link href={href} as={as}>
        <a>{`『${title}』`}</a>
      </Link>
    )
  }

  return (

    <div className={styles.targetList}>
       {targetBookList && (
          targetBookList.map(book => (
            <div key={book.id} className={styles.book}>
                {getBookLinkbyId(isFake, book.id, book.title)}
            </div>
          ))
      )}
    </div>
  );
}

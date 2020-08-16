import Link from 'next/link';
import styles from './commonQuoteList.module.scss'
export default function CommonQuoteList({ targetQuoteList, isFake=false }) {

  const getQuoteLinkInfo = (isFake, id) => (
    isFake ?
    {
      href:'/fake_quotes/[id]',
      as:`/fake_quotes/${id}`,
    } :
    {
      href:'/quotes/[id]/fake_quotes/list/[page]',
      as:`/quotes/${id}/fake_quotes/list/1`,
    }
  )
  const getQuoteLinkbyId = (isFake, id, text) => {
    const { href, as } = getQuoteLinkInfo(isFake, id)
    return (
      <Link href={href} as={as}>
        <a>{text}</a>
      </Link>
    )
  }

  return (
    <div className={styles.targetQuoteList}>
       {targetQuoteList && (
        <div className={styles.targetList}>
          {targetQuoteList.map(quote => (
            <div key={quote.id} className={styles.quote}>
                {getQuoteLinkbyId(isFake, quote.id, quote.text)}
            </div>
          ))}

        </div>
      )}
    </div>
  );
}

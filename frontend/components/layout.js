import Head from 'next/head'
import styles from './layout.module.css'
import utilStyles from '../styles/utils.module.css'
import Link from 'next/link'

const name = 'Your Name'
export const siteTitle = 'Next.js Sample Website'

export default function Layout({ children, home }) {
  return (
    <div className={styles.container}>
      <Head>
        <link rel="icon" href="/favicon.ico" />
        <meta
          name="description"
          content="Learn how to build a personal website using Next.js"
        />
        <meta
          property="og:image"
          content={`https://og-image.now.sh/${encodeURI(
            siteTitle
          )}.png?theme=light&md=0&fontSize=75px&images=https%3A%2F%2Fassets.zeit.co%2Fimage%2Fupload%2Ffront%2Fassets%2Fdesign%2Fnextjs-black-logo.svg`}
        />
        <meta name="og:title" content={siteTitle} />
        <meta name="twitter:card" content="summary_large_image" />
      </Head>
      <header className={styles.header}>
        {home ? (
          <>
            エセ文豪文庫
            {/* <h1 className={utilStyles.heading2Xl}>{name}</h1> */}
          </>
        ) : (
          <>
           <Link href="/">
            <a>エセ文豪文庫</a>
          </Link>
          </>
        )}
      </header>
      <main>{children}</main>
      {/* {!home && (
        <div className={styles.backToHome}>
          <Link href="/">
            <a>← Back to home</a>
          </Link>
        </div>
      )} */}
      <footer class="footer">
        <ul>
            <li>
            <Link href="/authors/list/[page]" as="/authors/list/1" >
            <a>原作一覧</a>
            </Link>
            </li>
            <li><a class="footer site-font-color" href="/fake_authors">エセ文豪一覧</a></li>
        </ul>
    </footer>


    </div>
  )
}
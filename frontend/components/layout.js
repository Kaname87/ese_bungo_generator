import Head from "next/head";

import Footer from "./footer";
import Header from "./header";
import { SITE_NAME } from "../config/const";

import styles from "./layout.module.scss";

const siteTitle = (text) => {
  if (text.length > 0) {
    return `${text} - ${SITE_NAME}`
  }
  return SITE_NAME
}

export default function Layout({ children, pageTitle='', randomIdList=[] }) {
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
            siteTitle(pageTitle)
          )}.png?theme=light&md=0&fontSize=75px&images=https%3A%2F%2Fassets.zeit.co%2Fimage%2Fupload%2Ffront%2Fassets%2Fdesign%2Fnextjs-black-logo.svg`}
        />
        <meta name="og:title" content={siteTitle(pageTitle)} />
        <meta name="twitter:card" content="summary_large_image" />
      </Head>
      <Header />
      <main className={styles.main}>{children}</main>
      {/* {!home && (
        <div className={styles.backToHome}>
          <Link href="/">
            <a>← Back to home</a>
          </Link>
        </div>
      )} */}
      <Footer randomIdList={randomIdList} />
    </div>
  );
}

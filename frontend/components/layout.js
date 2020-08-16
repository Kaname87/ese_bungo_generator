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
        <meta
          name="description"
          content="文豪の作品の名文を元に自動生成されたテキスト集です。文章中に使用された名詞に類似する名詞をランダムに置き換えることで文章を生成しています。"
        />
        <meta name="og:image" content="/images/ogp.png" />
        <meta name="og:title" content={siteTitle(pageTitle)} />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="keywords" content="文豪,名言,エセ,似非,Word2Vec" />

        <title>{siteTitle(pageTitle)}</title>
        <link rel="icon" href="/images/favicon.ico" />
        <link rel="apple-touch-icon" sizes="180x180" href="/images/apple-touch-icon.png" />

      </Head>
      <Header />
      <main className={styles.main}>{children}</main>

      <Footer randomIdList={randomIdList} />
    </div>
  );
}

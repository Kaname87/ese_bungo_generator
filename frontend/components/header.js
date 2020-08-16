import styles from "./header.module.scss";
import Link from 'next/link'
import { useRouter } from "next/router";
import { SITE_NAME } from "../config/const";

export default function Header({ }) {
  const router = useRouter()
  const isHome = router.pathname === '/'
  return (

    <header className={styles.header}>
      <div className={styles.serviceNameWrapper}>
      {isHome ? (
        <span className={styles.serviceName}>
            {SITE_NAME}
        </span>
      ) : (
        <Link href="/">
          <a className={styles.serviceName}>
              {SITE_NAME}
            </a>
        </Link>
      )}
      </div>
    </header>
  );
}

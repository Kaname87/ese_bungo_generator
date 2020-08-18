import Link from "next/link";
import { useRouter } from "next/router";
import { pickRandomData } from "../lib/util";

import styles from "./footer.module.scss";

export default function Footer({ randomIdList = [] }) {
  const router = useRouter();
  return (
    <footer className={styles.footer}>
      <ul>
        <li>
          {router.pathname === "/authors/list/[page]" ? (
            "原作一覧"
          ) : (
            <Link href="/authors/list/[page]" as="/authors/list/1">
              <a>原作一覧</a>
            </Link>
          )}
        </li>
        <li>
          {router.pathname === "/fake_authors/list/[page]" ? (
            "エセ文豪一覧"
          ) : (
            <Link href="/fake_authors/list/[page]" as="/fake_authors/list/1">
              <a>エセ文豪一覧</a>
            </Link>
          )}
        </li>
        <li>
          {router.pathname === "/fake_quotes/list/[page]" ? (
            "エセ引用一覧"
          ) : (
            <Link href="/fake_quotes/list/[page]" as="/fake_quotes/list/1">
              <a>エセ引用一覧</a>
            </Link>
          )}
        </li>
        {randomIdList.length > 0 && (
          <li>
            <a
              href="#"
              onClick={async (event) => {
                event.preventDefault();
                pickRandomData(randomIdList, router);
              }}
            >
              ランダムエセ引用
            </a>
          </li>
        )}
      </ul>
    </footer>
  );
}

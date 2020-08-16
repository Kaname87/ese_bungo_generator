import { useRouter } from "next/router";
import styles from "./randomButton.module.scss";
import { pickRandomData } from '../lib/util'

export default function  RandomButton({ idList }) {
  const router = useRouter();
  return (
    <a className={styles.random}
      onClick={
        (event) => {
            event.preventDefault()
            pickRandomData(idList, router)
        }
      }
    >
    ランダム
    </a>
  );
}

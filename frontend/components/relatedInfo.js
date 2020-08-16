import styles from "./relatedInfo.module.scss";

export default function RelatedInfo({ children}) {
  return (
    <div className={styles.info}>
        <div className={styles.line} />
        <h6 className={styles.head}>関連</h6>
        {children}
    </div>
  );
}

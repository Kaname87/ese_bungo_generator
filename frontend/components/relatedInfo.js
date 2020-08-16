import styles from "./relatedInfo.module.scss";

export default function RelatedInfo({
  children,
  head='関連',
  hideLineTop=false,
  hideLineBottom=false,
}) {

  return (
    <div className={styles.info}>
        {!hideLineTop && <div className={styles.line} />}
        <h6 className={styles.head}>{head}</h6>
        {children}
        {!hideLineBottom && <div className={styles.line} />}
    </div>
  );
}

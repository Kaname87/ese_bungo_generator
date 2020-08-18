import { useState } from "react";
import { PROFILE_IMAGE_LIST } from "../config/const";

import styles from "./profile.module.scss";

const setNextIdx = async (idx, setFunc) => {
  let nextIdx = idx + 1;
  if (nextIdx > PROFILE_IMAGE_LIST.length - 1) {
    nextIdx = 0;
  }
  setFunc(nextIdx);
};

export default function Profile({ profileIdx = 0, alt }) {
  const [imageIdx, setImageIdx] = useState(profileIdx);

  return (
    <div className={styles.fakeAuthor}>
      <img
        src={PROFILE_IMAGE_LIST[imageIdx]}
        onClick={async () => await setNextIdx(imageIdx, setImageIdx)}
        alt={alt}
      />
    </div>
  );
}

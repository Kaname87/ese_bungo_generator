import styles from "./twitterIcon.module.scss";
// import { SITE_URL } from "../config/const";
// TODO: This should be moved to Server Props to use env var
const SITE_URL = 'https://esebungo.vercel.app'

const getShareLink = (
  fakeAuthor,
  fakeBook,
  fakeQuote,
  hashtag = "エセ文豪"
) => {
  const url = encodeURIComponent(`${SITE_URL}/fake_quotes/${fakeQuote.id}`);
  const shareText = getShareText(fakeAuthor, fakeBook, fakeQuote);
  return `https://twitter.com/intent/tweet?text=${shareText}&hashtags=${hashtag}&url=${url}`;
};

const getShareText = (fakeAuthor, fakeBook, fakeQuote) => {
  const MAX_LENGTH = 95;
  let shareText = `${fakeQuote.text}\n\n${fakeAuthor.name}『${fakeBook.title}』`;
  if (shareText.length >= MAX_LENGTH) {
    const nameBookPart = `...\n\n${fakeAuthor.name}『${fakeBook.title}』`;
    const fakeQutePart = fakeQuote.text.slice(
      0,
      MAX_LENGTH - nameBookPart.length
    );
    shareText = fakeQutePart + nameBookPart;
  }
  return encodeURIComponent(shareText);
};

export default function TwitterIcon({ fakeAuthor, fakeBook, fakeQuote }) {
  return (
    <div className={styles.sns}>
      <a
        target="_blank"
        rel="noopener noreferrer"
        className={styles.twitterIcon}
        href={getShareLink(fakeAuthor, fakeBook, fakeQuote)}
      >
        Twitter
      </a>
    </div>
  );
}

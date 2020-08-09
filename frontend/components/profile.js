
import Head from 'next/head'
import styles from './layout.module.css'
import utilStyles from '../styles/utils.module.css'
import Link from 'next/link'

const name = 'Your Name'
export const siteTitle = 'Next.js Sample Website'

export default function Profile({ profileIdx = 0, alt }) {
    return (
        <div class="fake-author hide">
            <img
                src="/images/hayashi.jpg"
                // className={`${styles.headerHomeImage} ${utilStyles.borderCircle}`}
                alt={alt}
            />
        </div>
    );
};
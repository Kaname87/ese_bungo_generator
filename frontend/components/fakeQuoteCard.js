import Head from 'next/head'
import styles from './layout.module.css'
import utilStyles from '../styles/utils.module.css'
import Profile from './profile'
import Link from 'next/link'

const name = 'Your Name'
export const siteTitle = 'Next.js Sample Website'

export default function fakeQuoteCard({
    fakeQuote,
    fakeBook,
    fakeAuthor,
    quote,
    book,
    author
}) {
    return (
        <>
        <div class="fake">
            <div class="author-wrapper">
            <a class="page-controller prev-next" href="/fake_quotes/random/?fake_quote_id=">乱</a>
            <div class="fake-author" id="fake_author_profile">
            <Profile alt="エセ文豪著者近影" />
            </div>
            <a class="page-controller prev-next" href="/fake_quotes/random/?fake_quote_id=">乱</a>
            </div>

            <div class="novel">
            <p class="fake-quote">{fakeQuote.text}</p>
            <p class="fake-cite">
                <a href={"/fake_authors/" + fakeAuthor.name + "/fake_books"}>
                {fakeAuthor.name}
                </a>
                『{fakeBook.title}』
            </p>
            </div>
        </div>
        <div class="original">
            <blockquote>
            <a class="original-quote" href={"/original_quotes/" + quote.id + "/fake_quotes"}>
                {quote.text}
            </a>
            <cite class="original-cite">
                <a href={"/original_authors/" + author.name + "/fake_authors"}>
                {author.name}
                </a>
                <a href={"/books/" + book.id + "/quotes"}>『{book.title}』</a>
            </cite>
            </blockquote>
        </div>
    </>
    )
};
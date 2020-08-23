import fetch from 'node-fetch'
import { API_BASE_URL } from "../config/const"
export async function getFakeQuote(id) {
    const res = await fetch(`${API_BASE_URL}/fake_quotes/${id}`)

    const {
        fake_quote:fakeQuote,
        fake_book:fakeBook,
        fake_author:fakeAuthor,
        quote,
        book,
        author,
    } = await res.json()
    return {
        fakeQuote,
        fakeBook,
        fakeAuthor,
        quote,
        book,
        author,
    }
}

export async function getRandomFakeQuote(id=null) {
    let randomApi = `${API_BASE_URL}/fake_quotes/random`
    if (id) {
        randomApi += `?fake_quote_id=${id}`
    }
    const res = await fetch(randomApi)
    return res.json()
}

export async function getRandomFakeQuoteIdList(id=null) {
    let randomApi = `${API_BASE_URL}/fake_quotes/random_id_list?limit=5`
    if (id) {
        randomApi += `&fake_quote_id=${id}`
    }
    const res = await fetch(randomApi)
    return res.json()
}

export async function getAuthor(id) {
    const res = await fetch(`${API_BASE_URL}/authors/${id}`)
    return res.json()
}

export async function getFakeAuthor(id) {
    const res = await fetch(`${API_BASE_URL}/fake_authors/${id}`)
    return res.json()
}

//  List by parent
export async function getFakeAuthorListByAuthorId(authorId, offset=0, limit=100) {
    const res = await fetch(`${API_BASE_URL}/authors/${authorId}/fake_authors/list?offset=${offset}&limit=${limit}`)
    return res.json()
}

export async function getBookListByAuthorId(authorId, offset=0, limit=100) {
    const res = await fetch(`${API_BASE_URL}/authors/${authorId}/books/list?offset=${offset}&limit=${limit}`)
    return res.json()
}

export async function getQuoteListByBookId(bookId, offset=0, limit=100) {
    const res = await fetch(`${API_BASE_URL}/books/${bookId}/quotes/list?offset=${offset}&limit=${limit}`)
    return res.json()
}

export async function getFakeBookListByFakeAuthorId(fakeAuthorId, offset=0, limit=100) {
   const res = await fetch(`${API_BASE_URL}/fake_authors/${fakeAuthorId}/fake_books/list?offset=${offset}&limit=${limit}`)
   return res.json()
}

export async function getFakeQuoteListByQuoteId(quoteId, offset=0, limit=100) {
    const res = await fetch(`${API_BASE_URL}/quotes/${quoteId}/fake_quotes/list?offset=${offset}&limit=${limit}`)
    return res.json()
}
export async function getFakeQuoteListByFakeBookId(fakeBookId, offset=0, limit=100) {
    const res = await fetch(`${API_BASE_URL}/fake_books/${fakeBookId}/fake_quotes/list?offset=${offset}&limit=${limit}`)
    return res.json()
}


// All ID
function idListApi(resource, offset=0, limit=100) {
    return `${API_BASE_URL}/${resource}/id_list?offset=${offset}&limit=${limit}`
}

function listApi(resource, offset=0, limit=100) {
    return `${API_BASE_URL}/${resource}/list?offset=${offset}&limit=${limit}`
}

// ID LIST
export async function getAuthorIdList(offset=0, limit=100) {
    const res = await fetch(idListApi('authors', offset, limit))
    return res.json()
}

export async function getBookIdList(offset=0, limit=100) {
    const res = await fetch(idListApi('books', offset, limit))
    return res.json()
}

export async function getQuoteIdList(offset=0, limit=100) {
    const res = await fetch(idListApi('quotes', offset, limit))
    return res.json()
}

export async function getFakeAuthorIdList(offset=0, limit=100) {
    const res = await fetch(idListApi('fake_authors', offset, limit))
    return res.json()
}

export async function getFakeBookIdList(offset=0, limit=100) {
    const res = await fetch(idListApi('fake_books', offset, limit))
    return res.json()
}

export async function getFakeQuoteIdList(offset=0, limit=100) {
    const res = await fetch(idListApi('fake_quotes', offset, limit))
    return res.json()
}


// LIST
export async function getAuthorList(offset=0, limit=100) {
    const res = await fetch(listApi('authors', offset, limit))
    const {
        result_list:authorList,
        total,
    } = await res.json()

    return {
        authorList,
        total,
    }
}

export async function getFakeAuthorList(offset=0, limit=100) {
    const res = await fetch(listApi('fake_authors', offset, limit))
    return res.json()
}

export async function getFakeQuoteList(offset=0, limit=100) {
    const res = await fetch(listApi('fake_quotes', offset, limit))
    return res.json()
}
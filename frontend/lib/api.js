import fetch from 'node-fetch'

const API_BASE = 'http://127.0.0.1:5000/api';


export async function getFakeQuote(id) {
    const res = await fetch(`${API_BASE}/fake_quotes/${id}`)
    return res.json()
}

export async function getAuthor(id) {
    const res = await fetch(`${API_BASE}/authors/${id}`)
    return res.json()
}

export async function getFakeAuthor(id) {
    const res = await fetch(`${API_BASE}/fake_authors/${id}`)
    return res.json()
}

//  List by parent
export async function getFakeAuthorListByAuthorId(authorId, offset=0, limit=100) {
    const res = await fetch(`${API_BASE}/authors/${authorId}/fake_authors/list?offset=${offset}&limit=${limit}`)
    return res.json()
}

export async function getQuoteListByBookId(bookId, offset=0, limit=100) {
    const res = await fetch(`${API_BASE}/books/${bookId}/quotes/list?offset=${offset}&limit=${limit}`)
    return res.json()
}

export async function getFakeBookListByFakeAuthorId(fakeAuthorId, offset=0, limit=100) {
   const res = await fetch(`${API_BASE}/fake_authors/${fakeAuthorId}/fake_books/list?offset=${offset}&limit=${limit}`)
   return res.json()
}

export async function getFakeQuoteListByQuoteId(quoteId, offset=0, limit=100) {
    const res = await fetch(`${API_BASE}/quotes/${quoteId}/fake_quotes/list?offset=${offset}&limit=${limit}`)
    return res.json()
}
export async function getFakeQuoteListByFakeBookId(fakeBookId, offset=0, limit=100) {
    const res = await fetch(`${API_BASE}/fake_books/${fakeBookId}/fake_quotes/list?offset=${offset}&limit=${limit}`)
    return res.json()
}


// All ID
function idListApi(resource, offset=0, limit=100) {
    return `${API_BASE}/${resource}/id_list?offset=${offset}&limit=${limit}`
}

function listApi(resource, offset=0, limit=100) {
    return `${API_BASE}/${resource}/list?offset=${offset}&limit=${limit}`
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
    return res.json()
}

export async function getFakeAuthorList(offset=0, limit=100) {
    const res = await fetch(listApi('fake_authors', offset, limit))
    return res.json()
}

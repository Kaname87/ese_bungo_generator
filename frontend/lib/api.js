import fetch from 'node-fetch'

const API_BASE = 'http://127.0.0.1:5000/api';

export async function getSortedPostsData() {
    const res = await fetch(`${API_BASE}/fake_quotes/random`)
    return res.json()
}

export async function getFakeQuote(id) {
    const res = await fetch(`${API_BASE}/fake_quotes/${id}`)
    return res.json()
}

export async function getAuthor(id) {
    const res = await fetch(`${API_BASE}/authors/${id}`)
    return res.json()
}

//  List by parent
export async function getFakeAuthorListByAuthorId(authorId) {
    const res = await fetch(`${API_BASE}/authors/${authorId}/fake_authors/list`)
    return res.json()
}

export async function getFakeBookListByFakeAuthorId(fakeAuthorId) {
    const res = await fetch(`${API_BASE}/fake_authors/${fakeAuthorId}/fake_books/list`)
    return res.json()
}

export async function getQuoteListByBookId(bookId) {
    const res = await fetch(`${API_BASE}/books/${bookId}/quotes/list`)
    return res.json()
}

export async function getFakeQuoteListByQuoteId(quoteId) {
    const res = await fetch(`${API_BASE}/quotes/${quoteId}/fake_quotes/list`)
    return res.json()
}

// All ID
function idListApi(resource, offset=0, limit=100) {
    return `${API_BASE}/${resource}/id_list?offset=${offset}&limit=${limit}`
}

function listApi(resource, offset=0, limit=100) {
    return `${API_BASE}/${resource}/list?offset=${offset}&limit=${limit}`
}

export async function getFakeQuoteIdList(offset=0, limit=100) {
    const res = await fetch(idListApi('fake_quotes', offset, limit))
    return res.json()
}

export async function getAuthorIdList(offset=0, limit=100) {
    const res = await fetch(idListApi('authors', offset, limit))
    return res.json()
}

export async function getAuthorList(offset=0, limit=100) {
    const res = await fetch(listApi('authors', offset, limit))
    return res.json()
}

export async function getFakeAuthorIdList(offset=0, limit=100) {
    const res = await fetch(idListApi('fake_authors', offset, limit))
    return res.json()
}

export async function recFetchIdList(fn, offset=0, totalIdList=[]) {
    const {
        id_list: idList,
        next_offset: nextOffset
    } = await fn(offset);

    if (nextOffset < 0)  {
        return totalIdList.concat(idList);
    }
    await delay(2)
    return await recFetchIdList(fn, nextOffset, totalIdList.concat(idList));
}

async function delay(t) {
    return new Promise(resolve => setTimeout(resolve, t));
}
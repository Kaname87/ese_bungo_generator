import { IncomingMessage } from "http";
import { parse } from "url";

export function parseRequest(req: IncomingMessage) {
  const { query = {} } = parse(req.url || "", true);
  const {
    author,
    book,
    quote,
    fakeAuthor,
    fakeBook,
    fakeQuote,
    profileName,
  } = query;

  if (Array.isArray(author)) {
    throw new Error("Author can't be array");
  }
  if (Array.isArray(book)) {
    throw new Error("Book can't be array");
  }
  if (Array.isArray(quote)) {
    throw new Error("Quote can't be array");
  }
  if (Array.isArray(fakeAuthor)) {
    throw new Error("FakeAuthor can't be array");
  }
  if (Array.isArray(fakeBook)) {
    throw new Error("FakeBook can't be array");
  }
  if (Array.isArray(fakeQuote)) {
    throw new Error("FakeQuote can't be array");
  }
  if (Array.isArray(profileName)) {
    throw new Error("profileName can't be array");
  }

  const parsedReq: ParsedRequest = {
    author,
    book,
    quote,
    fakeAuthor,
    fakeBook,
    fakeQuote,
    profileName,
  };

  return parsedReq;
}

from app import db
from sqlalchemy.dialects.postgresql import UUID

class Author(db.Model):
    __tablename__ = "authors"
    __table_args__ = {'extend_existing': True}

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    name = db.Column(db.String(), nullable=False)

    # Relation
    fake_authors = db.relationship("FakeAuthor",  backref="authors") # Has many
    books = db.relationship("Book", backref="authors") # Has many

    def __init__(self, name):
        self.name = name

class Book(db.Model):
    __tablename__ = "books"
    __table_args__ = {'extend_existing': True}

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey('authors.id'))

    title = db.Column(db.String(), nullable=False)
    url = db.Column(db.String(), nullable=False)

    # Relation
    author = db.relationship("Author",  back_populates="books") # Has One
    quotes  = db.relationship("Quote",  backref="books") # Has Many
    fake_books = db.relationship("FakeBook",  backref="books") # Has Many

    def __init__(self, title, url):
        self.title = title
        self.url = url

class Quote(db.Model):
    __tablename__ = "quotes"
    __table_args__ = {'extend_existing': True}

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    book_id = db.Column(UUID(as_uuid=True), db.ForeignKey('books.id'))

    text = db.Column(db.String(), nullable=False)

    # Relation
    book = db.relationship("Book",  back_populates="quotes")  # Has One
    fake_quotes = db.relationship("FakeQuote",  backref="quotes")  # Has Many

    def __init__(self, text):
        self.text = text

class FakeAuthor(db.Model):
    __tablename__ = "fake_authors"
    __table_args__ = {'extend_existing': True}

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey('authors.id'))
    name = db.Column(db.String(), nullable=False)

    # Relation
    original_author = db.relationship("Author",  back_populates="fake_authors") # Has One

    def __init__(self, author_id, name):
        self.author_id = author_id
        self.name = name


class FakeBook(db.Model):
    __tablename__ = "fake_books"
    __table_args__ = {'extend_existing': True}

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    book_id = db.Column(UUID(as_uuid=True), db.ForeignKey('books.id'))
    title = db.Column(db.String(), nullable=False)

    # Relation
    original_book = db.relationship("Book",  back_populates="fake_books") # Has One
    fake_quotes = db.relationship("FakeQuote",  backref="fake_books") # Has Many

    def __init__(self, book_id, title):
        self.book_id = book_id
        self.title = title

class FakeQuote(db.Model):
    __tablename__ = "fake_quotes"
    __table_args__ = {'extend_existing': True}

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    quote_id = db.Column(UUID(as_uuid=True), db.ForeignKey('quotes.id'))
    fake_book_id = db.Column(UUID(as_uuid=True), db.ForeignKey('fake_books.id'))
    text = db.Column(db.String(), nullable=False)

    # Relation
    original_quote = db.relationship("Quote",  back_populates="fake_quotes") # Has One
    fake_book = db.relationship("FakeBook",  back_populates="fake_quotes") # Has One

    def __init__(self, quote_id, text):
        self.quote_id = quote_id
        self.text = text


# CREATE TABLE authors (
#   id uuid DEFAULT uuid_generate_v4(),
#   name varchar(100) NOT NULL,
#   PRIMARY KEY(id)
# );
# -- INSERT INTO authors (name) VALUES ('芥川');

# CREATE TABLE fake_authors (
#   id uuid DEFAULT uuid_generate_v4(),
#   author_id uuid NOT NULL,
#   name varchar(100) NOT NULL,
#   PRIMARY KEY(id),
#   CONSTRAINT fk_original_author
#     FOREIGN KEY(author_id)
#       REFERENCES authors(id)
# );
# -- INSERT INTO fake_authors (author_id, name) VALUES ('b30aa811-f8a4-43b0-bfc0-a3ff59623783', '芥川');

# CREATE TABLE books (
#   id uuid DEFAULT uuid_generate_v4(),
#   author_id uuid NOT NULL,
#   title varchar(250) NOT NULL,
#   url varchar(250) NOT NULL,
#   PRIMARY KEY(id),
#   CONSTRAINT fk_author
#     FOREIGN KEY(author_id)
#       REFERENCES authors(id)
# );
# -- INSERT INTO books (title, url) VALUES ('芥川book', 'http://test');

# CREATE TABLE fake_books (
#   id uuid DEFAULT uuid_generate_v4(),
#   book_id uuid NOT NULL,
#   title varchar(250) NOT NULL,
#   PRIMARY KEY(id),
#   CONSTRAINT fk_original_book
#     FOREIGN KEY(book_id)
#     REFERENCES books(id)
# );

# -- INSERT INTO fake_books (book_id, title) VALUES ('7d92edd8-73f4-45cf-992a-1ceb5cbb4136', 'nise芥川');


# CREATE TABLE quotes (
#   id uuid DEFAULT uuid_generate_v4(),
#   book_id uuid NOT NULL,
#   text text NOT NULL,
#   PRIMARY KEY(id),
#   CONSTRAINT fk_book
#     FOREIGN KEY(book_id)
#       REFERENCES books(id)
# );

# CREATE TABLE fake_quotes (
#   id uuid DEFAULT uuid_generate_v4(),
#   quote_id uuid NOT NULL,
#   text text NOT NULL,
#   PRIMARY KEY(id),
#   CONSTRAINT fk_original_quote
#     FOREIGN KEY(quote_id)
#       REFERENCES quotes(id)
# );
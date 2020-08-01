from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

# local modules
from database import Base

# CREATE TABLE authors (
#   id uuid DEFAULT uuid_generate_v4(),
#   name varchar(100) NOT NULL,
#   PRIMARY KEY(id)
# );
class Author(Base):
    __tablename__ = "authors"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(), nullable=False)

    # Relation
    fake_authors = relationship("FakeAuthor", backref="authors") # Has many
    books = relationship("Book", backref="authors") # Has many

    def __init__(self, name):
        self.name = name

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
class Book(Base):
    __tablename__ = "books"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey('authors.id'))

    title = Column(String(), nullable=False)
    url = Column(String(), nullable=False)

    # Relation
    author = relationship("Author", back_populates="books") # Has One
    quotes  = relationship("Quote", backref="books") # Has Many
    fake_books = relationship("FakeBook", backref="books") # Has Many

    def __init__(self, title, url):
        self.title = title
        self.url = url


# CREATE TABLE quotes (
#   id uuid DEFAULT uuid_generate_v4(),
#   book_id uuid NOT NULL,
#   text text NOT NULL,
#   PRIMARY KEY(id),
#   CONSTRAINT fk_book
#     FOREIGN KEY(book_id)
#       REFERENCES books(id)
# );
class Quote(Base):
    __tablename__ = "quotes"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True)
    book_id = Column(UUID(as_uuid=True), ForeignKey('books.id'))

    text = Column(String(), nullable=False)

    # Relation
    book = relationship("Book", back_populates="quotes")  # Has One
    fake_quotes = relationship("FakeQuote", backref="quotes")  # Has Many

    def __init__(self, text):
        self.text = text

# CREATE TABLE fake_authors (
#   id uuid DEFAULT uuid_generate_v4(),
#   author_id uuid NOT NULL,
#   name varchar(100) NOT NULL,
#   PRIMARY KEY(id),
#   CONSTRAINT fk_original_author
#     FOREIGN KEY(author_id)
#       REFERENCES authors(id)
# );
class FakeAuthor(Base):
    __tablename__ = "fake_authors"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey('authors.id'))
    name = Column(String(), nullable=False)

    # Relation
    original_author = relationship("Author", back_populates="fake_authors") # Has One
    fake_books = relationship("FakeBook", backref="fake_authors") # Has Many

    def __init__(self, author_id, name):
        self.author_id = author_id
        self.name = name

# CREATE TABLE fake_books (
#   id uuid DEFAULT uuid_generate_v4(),
#   book_id uuid NOT NULL,
#   title varchar(250) NOT NULL,
#   PRIMARY KEY(id),
#   CONSTRAINT fk_original_book
#     FOREIGN KEY(book_id)
#     REFERENCES books(id)
# );
class FakeBook(Base):
    __tablename__ = "fake_books"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True)
    book_id = Column(UUID(as_uuid=True), ForeignKey('books.id'))
    fake_author_id = Column(UUID(as_uuid=True), ForeignKey('fake_authors.id'))
    title = Column(String(), nullable=False)

    # Relation
    original_book = relationship("Book", back_populates="fake_books") # Has One

    fake_author = relationship("FakeAuthor", back_populates="fake_books") # Has One

    fake_quotes = relationship("FakeQuote", backref="fake_books") # Has Many

    def __init__(self, book_id, title):
        self.book_id = book_id
        self.title = title


# CREATE TABLE fake_quotes (
#   id uuid DEFAULT uuid_generate_v4(),
#   quote_id uuid NOT NULL,
#   text text NOT NULL,
#   PRIMARY KEY(id),
#   CONSTRAINT fk_original_quote
#     FOREIGN KEY(quote_id)
#       REFERENCES quotes(id)
# );
class FakeQuote(Base):
    __tablename__ = "fake_quotes"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True)
    quote_id = Column(UUID(as_uuid=True), ForeignKey('quotes.id'))
    fake_book_id = Column(UUID(as_uuid=True), ForeignKey('fake_books.id'))
    text = Column(String(), nullable=False)

    # Relation
    original_quote = relationship("Quote", back_populates="fake_quotes") # Has One
    fake_book = relationship("FakeBook", back_populates="fake_quotes") # Has One

    def __init__(self, quote_id, text):
        self.quote_id = quote_id
        self.text = text

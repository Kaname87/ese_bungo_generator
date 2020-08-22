from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, class_mapper
from sqlalchemy.dialects.postgresql import UUID

from web.database import Base

class AppBase(Base):
    __abstract__ = True
    __table_args__ = {'extend_existing': True}

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())

    def to_dict(self):
        cls = self.__class__
        convert = dict()
        d = dict()
        for c in cls.__table__.columns:
            v = getattr(self, c.name)
            if c.type in convert.keys() and v is not None:
                try:
                    d[c.name] = convert[c.type](v)
                except:
                    d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
            elif v is None:
                d[c.name] = str()
            else:
                d[c.name] = v
        return d


# CREATE TABLE authors (
#   id UUID DEFAULT uuid_generate_v4(),
#   name VARCHAR(100) COLLATE "ja-x-icu" NOT NULL,
#   name_kana VARCHAR(100) COLLATE "ja-x-icu" NOT NULL,
#   created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
#   updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY(id)
# );
class Author(AppBase):
    __tablename__ = "authors"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(collation='ja-x-icu'), nullable=False)
    name_kana = Column(String(collation='ja-x-icu'), nullable=False)

    # Relation
    fake_authors = relationship("FakeAuthor", backref="authors") # Has many
    books = relationship("Book", backref="authors") # Has many

    def __init__(self, name, name_kana):
        self.name = name
        self.name_kana = name_kana

# CREATE TABLE books (
#   id UUID DEFAULT uuid_generate_v4(),
#   author_id UUID NOT NULL,
#   title VARCHAR(250) COLLATE "ja-x-icu" NOT NULL,
#   url VARCHAR(250) NOT NULL,
#   created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
#   updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY(id),
#   CONSTRAINT fk_author
#     FOREIGN KEY(author_id)
#       REFERENCES authors(id)
# );
class Book(AppBase):
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey('authors.id'))
    title = Column(String(collation='ja-x-icu'), nullable=False)
    url = Column(String(), nullable=False)

    # Relation
    author = relationship("Author", back_populates="books") # Has One
    quotes  = relationship("Quote", backref="books") # Has Many
    fake_books = relationship("FakeBook", backref="books") # Has Many

    def __init__(self, title, url):
        self.title = title
        self.url = url



# CREATE TABLE quotes (
#   id UUID DEFAULT uuid_generate_v4(),
#   book_id UUID NOT NULL,
#   text TEXT COLLATE "ja-x-icu" NOT NULL,
#   created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
#   updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY(id),
#   CONSTRAINT fk_book
#     FOREIGN KEY(book_id)
#       REFERENCES books(id)
# );
class Quote(AppBase):
    __tablename__ = "quotes"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True)
    book_id = Column(UUID(as_uuid=True), ForeignKey('books.id'))
    text = Column(String(collation='ja-x-icu'), nullable=False)

    # Relation
    book = relationship("Book", back_populates="quotes")  # Has One
    fake_quotes = relationship("FakeQuote", backref="quotes")  # Has Many

    def __init__(self, text):
        self.text = text


# CREATE TABLE fake_authors (
#   id UUID DEFAULT uuid_generate_v4(),
#   author_id UUID NOT NULL,
#   name varchar(100) COLLATE "ja-x-icu" NOT NULL,
#   created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
#   updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY(id),
#   CONSTRAINT fk_original_author
#     FOREIGN KEY(author_id)
#       REFERENCES authors(id)
# );
class FakeAuthor(AppBase):
    __tablename__ = "fake_authors"

    id = Column(UUID(as_uuid=True), primary_key=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey('authors.id'))
    name = Column(String(collation='ja-x-icu'), nullable=False)

    # Relation
    original_author = relationship("Author", back_populates="fake_authors") # Has One
    fake_books = relationship("FakeBook", backref="fake_authors") # Has Many

    def __init__(self, author_id, name):
        self.author_id = author_id
        self.name = name


# CREATE TABLE fake_books (
#   id UUID DEFAULT uuid_generate_v4(),
#   book_id UUID NOT NULL,
#   fake_author_id UUID NOT NULL,
#   title VARCHAR(250) COLLATE "ja-x-icu" NOT NULL,
#   created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
#   updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY(id),
#   CONSTRAINT fk_original_book
#     FOREIGN KEY(book_id)
#     REFERENCES books(id),
#   CONSTRAINT fk_fake_author
#     FOREIGN KEY(fake_author_id)
#       REFERENCES fake_authors(id)
# );
class FakeBook(AppBase):
    __tablename__ = "fake_books"

    id = Column(UUID(as_uuid=True), primary_key=True)
    book_id = Column(UUID(as_uuid=True), ForeignKey('books.id'))
    fake_author_id = Column(UUID(as_uuid=True), ForeignKey('fake_authors.id'))
    title = Column(String(collation='ja-x-icu'), nullable=False)

    # Relation
    original_book = relationship("Book", back_populates="fake_books") # Has One
    fake_author = relationship("FakeAuthor", back_populates="fake_books") # Has One
    fake_quotes = relationship("FakeQuote", backref="fake_books") # Has Many

    def __init__(self, book_id, title):
        self.book_id = book_id
        self.title = title


# CREATE TABLE fake_quotes (
#   id UUID DEFAULT uuid_generate_v4(),
#   quote_id UUID NOT NULL,
#   fake_book_id UUID NOT NULL,
#   text TEXT COLLATE "ja-x-icu" NOT NULL,
#   created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
#   updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY(id),
#   CONSTRAINT fk_original_quote
#     FOREIGN KEY(quote_id)
#       REFERENCES quotes(id),
#   CONSTRAINT fk_fake_book
#     FOREIGN KEY(fake_book_id)
#       REFERENCES fake_books(id)
# );
class FakeQuote(AppBase):
    __tablename__ = "fake_quotes"

    id = Column(UUID(as_uuid=True), primary_key=True)
    quote_id = Column(UUID(as_uuid=True), ForeignKey('quotes.id'))
    fake_book_id = Column(UUID(as_uuid=True), ForeignKey('fake_books.id'))
    text = Column(String(collation='ja-x-icu'), nullable=False)

    # Relation
    original_quote = relationship("Quote", back_populates="fake_quotes") # Has One
    fake_book = relationship("FakeBook", back_populates="fake_quotes") # Has One

    def __init__(self, quote_id, text):
        self.quote_id = quote_id
        self.text = text

import os

from uuid import UUID
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy import func, exc
import sys

# from sqlalchemy.exc import SQLAlchemyError


dotenv_path = os.path.dirname(__file__) + '/.env'
load_dotenv(dotenv_path)

app = Flask(__name__)

app.config.from_object(os.environ.get('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def is_uuid(uuid_string, version=4):
    try:
        val = UUID(uuid_string, version=version)
    except ValueError:
        return False
    return True

def render_quote_detail(fake_quote):
    from models import FakeAuthor
    fake_book = fake_quote.fake_book

    # Original
    quote = fake_quote.original_quote
    book = quote.book
    author= book.author

    fake_author = None
    fake_author_id =  request.args.get('fake_author_id', '')
    print('fake_author_id', fake_author_id)

    # from sqlalchemy.dialects.postgresql import UUID
    # fake_author_id = UUID.(fake_author_id)
    # print(UUID(fake_author_id))

    print('***************************')
    print(fake_author_id)
    print(is_uuid(fake_author_id))

    if is_uuid(fake_author_id):
        fake_author = FakeAuthor.query.filter_by(
            id=fake_author_id,
            author_id=author.id
        ).first()

        print('--------')
        print(fake_author)

    if fake_author is None:
        # Pick Random Fake Author by author_id
        # (No direct relation between FakeAuthor and FakeBook)
        fake_author = FakeAuthor.query.filter_by(author_id=author.id).order_by(func.random()).first()

    return render_template('index.html',
        author=author,
        book=book,
        quote=quote,
        fake_author=fake_author,
        fake_book=fake_book,
        fake_quote=fake_quote
    )
@app.route("/")
def show_random_quote():
    from models import FakeQuote

    # Pick Random Fake Quote
    fake_quote = FakeQuote.query.order_by(func.random()).first()
    return render_quote_detail(fake_quote)

@app.route('/bungo_list')
def list_authors():
    from models import Author
    authors = Author.query.order_by(Author.name).all()
    return render_template('list.html', authors=authors)

@app.route('/esebungo_list')
def list_fake_authors():
    from models import FakeAuthor
    fake_authors = FakeAuthor.query.order_by(FakeAuthor.name).all()
    return render_template('fake_list.html', fake_authors=fake_authors)

@app.route('/bungo/<author_name>/esebungo_list')
def list_all_fake_books(author_name):
    from models import Author
    from models import FakeBook
    author = Author.query.filter_by(name=author_name).first()

    return render_template('fake_list.html', fake_authors=author.fake_authors, author=author)
    # return render_template('related_fake_author_list.html', author=author)

@app.route('/ese_bungo/<fake_author_id>')
def list_fake_books(fake_author_id):
    from models import FakeAuthor
    fake_author = FakeAuthor.query.filter_by(id=fake_author_id).first()

    return render_template('fake_book_list.html', fake_author=fake_author)

@app.route('/ese_meigen/<fake_quote_id>')
def show_fake_quote(fake_quote_id):
    from models import FakeQuote
    fake_quote = FakeQuote.query.filter_by(id=fake_quote_id).first()
    return render_quote_detail(fake_quote)


if __name__ == '__main__':
    # app = create_app()
    app.run()


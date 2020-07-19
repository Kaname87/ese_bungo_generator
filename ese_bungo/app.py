import os

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from sqlalchemy import func


dotenv_path = os.path.dirname(__file__) + '/.env'
load_dotenv(dotenv_path)

app = Flask(__name__)

app.config.from_object(os.environ.get('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/")
def random():
    # from models import Author
    from models import FakeAuthor
    # from models import Book
    # from models import FakeBook
    from models import Quote
    from models import FakeQuote

    # Pick Random Fake Quote
    fake_quote = FakeQuote.query.order_by(func.random()).first()
    fake_book = fake_quote.fake_book

    # Original
    quote = fake_quote.original_quote
    book = quote.book
    author= book.author

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

if __name__ == '__main__':
    # app = create_app()
    app.run()


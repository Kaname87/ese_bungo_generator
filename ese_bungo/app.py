import os

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


dotenv_path = os.path.dirname(__file__) + '/.env'
# dotenv_path = Path('.') / '.env'
# print(dotenv_path)
load_dotenv(dotenv_path)

app = Flask(__name__)

app.config.from_object(os.environ.get('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/")
def hello():
    from models import Author
    author = Author.query
    print(author)
    # print(author.fake_authors)

    entries = []
    return render_template('index.html', entries=entries)

if __name__ == '__main__':
    # app = create_app()
    app.run()




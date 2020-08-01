import os
import sys
import random
import urllib.parse

from sqlalchemy import func, exc
from flask import Flask, request, render_template, redirect, url_for, _app_ctx_stack, abort, flash
from flask_cors import CORS
from sqlalchemy.orm import scoped_session
from flask_paginate import Pagination, get_page_parameter

# local modules
from database import SessionLocal, engine
import util
import models
import config

PER_PAGE = 30
def create_app():
    models.Base.metadata.create_all(bind=engine)
    util.load_env()

    app = Flask(__name__)
    CORS(app)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

    @app.route('/')
    def show_random_quote():
        # Pick Random Fake Quote
        fake_quote = app.session.query(models.FakeQuote).order_by(func.random()).first()

        twitter_share = get_twitter_share_info(fake_quote)
        return render_template('index.html', fake_quote=fake_quote, twitter_share=twitter_share)

    @app.route('/ese_meigen/<fake_quote_id>')
    def show_fake_quote(fake_quote_id):

        # When invalid id is passed, just redirect to random page
        if not util.is_uuid(fake_quote_id):
            return redirect(url_for('show_random_quote'))
        fake_quote = app.session.query(models.FakeQuote).filter_by(id=fake_quote_id).first()
        if fake_quote == None:
            return redirect(url_for('show_random_quote'))

        twitter_share = get_twitter_share_info(fake_quote)
        return render_template('index.html',fake_quote=fake_quote, twitter_share=twitter_share)

    @app.route('/bungo/list')
    def list_authors():
        page = request.args.get(get_page_parameter(), type=int, default=1)
        offset = PER_PAGE * (page-1)
        authors = app.session.query(models.Author) \
            .order_by(models.Author.name) \
            .offset(offset) \
            .limit(PER_PAGE) \
            .all()

        pagination = get_pagenate(page, models.Author)
        return render_template('list.html', authors=authors, pagination=pagination)

    @app.route('/ese_bungo/list')
    def list_fake_authors():
        page = request.args.get(get_page_parameter(), type=int, default=1)
        offset = PER_PAGE * (page-1)
        fake_authors = app.session.query(models.FakeAuthor) \
            .order_by(models.FakeAuthor.name) \
            .offset(offset) \
            .limit(PER_PAGE) \
            .all()

        pagination = get_pagenate(page, models.FakeAuthor)
        return render_template('fake_list.html', fake_authors=fake_authors, pagination=pagination)

    @app.route('/bungo/<author_name>/ese_list')
    def list_all_fake_books(author_name):
        page = request.args.get(get_page_parameter(), type=int, default=1)
        offset = PER_PAGE * (page-1)

        author = app.session.query(models.Author).filter_by(name=author_name).first()
        if author == None:
            flash(random_not_found_message(author_name))
            return abort(404)

        query_filter = (models.FakeAuthor.author_id==author.id)
        pagination = get_pagenate(page, models.FakeAuthor, query_filter)
        return render_template('fake_list.html', fake_authors=author.fake_authors, pagination=pagination)

    @app.route('/ese_bungo/<fake_author_name>/novels')
    def list_fake_books(fake_author_name):
        fake_author = app.session.query(models.FakeAuthor).filter_by(name=fake_author_name).first()
        if fake_author == None:
            flash(random_not_found_message(fake_author_name))
            return abort(404)
        return render_template('fake_book_list.html', fake_author=fake_author)

    @app.errorhandler(404)
    def not_found(e):
        print(e)
        return render_template('404.html')

    if os.environ['FLASK_ENV'] == 'production':
        @app.errorhandler(Exception)
        def handle_exception(e):
            print(e)
            app.session.rollback()
            return render_template('500.html')

    @app.teardown_appcontext
    def remove_session(*args, **kwargs):
        app.session.remove()

    # Utility functions
    def random_not_found_message(name):
        #　これも生成する？
        message = random.choice([
            'なぞ聞いたことありませんね',
            'の取り扱いはありません',
            '...？それって有名な人？'
        ])
        return '{}{}'.format(name, message)

    def get_pagenate(page, model_class, filters=None):
        msg = " " # "全{total}人中 {start} - {end}人表示中</b>"

        query = app.session.query(model_class)
        if filters is not None:
            query = query.filter(filters)

        total = query.count()

        record_name = model_class.__table__.name
        pagination = Pagination(page=page, display_msg=msg, per_page=PER_PAGE, total=total, record_name=record_name)
        return pagination

    def get_twitter_share_info(fake_quote):
        MAX_LENGTH = 100
        share_url = urllib.parse.quote(
            url_for('show_fake_quote', fake_quote_id=fake_quote.id, _external=True)
        )
        text = '{}\n\n{}『{}』\n'.format(fake_quote.text, fake_quote.fake_book.fake_author.name, fake_quote.fake_book.title)
        if len(text) >= MAX_LENGTH:
            text  = text[:MAX_LENGTH] + '...\n'

        share_text = urllib.parse.quote(text)
        return {
            'url': share_url,
            'text': share_text
        }

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()


import os
import sys
import random
import urllib.parse

from flask import Flask, request, render_template, redirect, url_for, _app_ctx_stack, abort, flash, jsonify
from flask_caching import Cache
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import func, exc, and_
from sqlalchemy.orm import scoped_session, contains_eager
# from sqlalchemy.sql import in_

from web import util, models, config
from web.database import SessionLocal, engine

PER_PAGE = 12
CHILDREN_LIMIT = 3

def create_app():
    models.Base.metadata.create_all(bind=engine)
    util.load_env()

    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

    cache = Cache(app, {'CACHE'})

    @app.route('/')
    def show_random_quote():
        # Pick Random Fake Quote
        fake_quote = app.session.query(models.FakeQuote).order_by(func.random()).first()
        return render_fake_quote_page(fake_quote)

    @app.route('/fake_quotes/<fake_quote_id>')
    @cache.cached(query_string=True)
    def show_fake_quote(fake_quote_id):
        # When invalid id is passed, just redirect to random page
        if not util.is_uuid(fake_quote_id):
            return redirect(url_for('show_random_quote'))
        fake_quote = app.session.query(models.FakeQuote).filter(models.FakeQuote.id==fake_quote_id).first()
        if fake_quote == None:
            return redirect(url_for('show_random_quote'))

        return render_fake_quote_page(fake_quote)

    @app.route('/original_authors')
    @cache.cached(query_string=True)
    def list_authors():
        page = get_page()
        offset = get_offset(page)

        authors = app.session.query(models.Author) \
            .order_by(models.Author.name_kana) \
            .offset(offset) \
            .limit(PER_PAGE) \
            .all()

        for author in authors:
            books = app.session.query(models.Book) \
                .filter(models.Book.author_id==author.id) \
                .order_by(models.Book.title) \
                .limit(CHILDREN_LIMIT) \
                .all()
            setattr(author, 'books', books)

            book_count = app.session.query(models.Book) \
                .filter(models.Book.author_id==author.id) \
                .count()
            setattr(author, 'book_count', book_count)


        pagination = get_pagenate(page, models.Author)
        return render_template('original_author_list.html', authors=authors, pagination=pagination)

    @app.route('/fake_authors')
    @cache.cached(query_string=True)
    def list_fake_authors():
        page = get_page()
        offset = get_offset(page)

        fake_authors = app.session.query(models.FakeAuthor) \
            .order_by(models.FakeAuthor.name) \
            .offset(offset) \
            .limit(PER_PAGE) \
            .all()
        return render_fake_author_book_list(page, '', fake_authors)

    def render_fake_author_book_list(page, author, fake_authors, query_filter=None):
        for fake_author in fake_authors:
            fake_books = app.session.query(models.FakeBook) \
                .filter(models.FakeBook.fake_author_id==fake_author.id) \
                .order_by(models.FakeBook.title) \
                .limit(CHILDREN_LIMIT) \
                .all()
            setattr(fake_author, 'fake_books', fake_books)

            fake_book_count = app.session.query(models.FakeBook) \
                .filter(models.FakeBook.fake_author_id==fake_author.id) \
                .count()
            setattr(fake_author, 'fake_book_count', fake_book_count)

        pagination = get_pagenate(page, models.FakeAuthor, query_filter)
        return render_template('fake_list.html', fake_authors=fake_authors, author=author, pagination=pagination)


    @app.route('/original_authors/<author_name>/fake_authors')
    @cache.cached(query_string=True)
    def list_all_fake_books(author_name):
        page = get_page()
        offset = get_offset(page)

        author = app.session.query(models.Author).filter_by(name=author_name).first()
        if author == None:
            flash(random_not_found_message(author_name))
            return abort(404)

        fake_authors = app.session.query(models.FakeAuthor) \
            .filter(models.FakeAuthor.author_id==author.id) \
            .order_by(models.FakeAuthor.name) \
            .offset(offset) \
            .limit(PER_PAGE) \
            .all()

        query_filter = (models.FakeAuthor.author_id==author.id)
        return render_fake_author_book_list(page, author, fake_authors, query_filter)

    @app.route('/fake_authors/<fake_author_name>/fake_books')
    @cache.cached(query_string=True)
    def list_fake_books(fake_author_name):
        fake_author = app.session.query(models.FakeAuthor).filter_by(name=fake_author_name).first()
        if fake_author == None:
            flash(random_not_found_message(fake_author_name))
            return abort(404)

        page = page = get_page()
        offset = get_offset(page)
        query_filter = (models.FakeBook.fake_author_id==fake_author.id)

        # .order_by(asc(collate(models.FakeBook.title, 'ja-x-icu'))) \
        fake_books = app.session.query(models.FakeBook) \
            .filter(query_filter) \
            .order_by(models.FakeBook.title) \
            .offset(offset) \
            .limit(PER_PAGE) \
            .all()

        pagination = get_pagenate(page, models.FakeBook, query_filter)
        return render_template('fake_book_list.html', fake_author=fake_author, fake_books=fake_books, pagination=pagination)


# http://127.0.0.1:5000/books/74969e90-f19b-4d48-8857-e8cc94496c0c/fake_books
    @app.route('/books/<book_id>/fake_books')
    @cache.cached(query_string=True)
    def list_fake_books_by_book(book_id):
        if not util.is_uuid(book_id):
            return redirect(url_for('show_random_quote'))

        book = app.session.query(models.Book) \
            .filter_by(id=book_id).first()

        if book == None:
            return redirect(url_for('show_random_quote'))

        page = page = get_page()
        offset = get_offset(page)
        query_filter = (models.FakeBook.book_id==book_id)

        fake_books = app.session.query(models.FakeBook) \
            .filter(query_filter) \
            .order_by(models.FakeBook.title) \
            .offset(offset) \
            .limit(PER_PAGE) \
            .all()

        pagination = get_pagenate(page, models.FakeBook, query_filter)
        return render_template('fake_book_list2.html', book=book, fake_books=fake_books, pagination=pagination)

    @app.errorhandler(404)
    def not_found(e):
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
            'は聞いたことがありませんね',
            'の取り扱いはありません',
            '...？有名な人？'
        ])
        return '{}{}'.format(name, message)

    @cache.memoize()
    def get_pagenate(page, model_class, filters=None):
        msg = " " # "全{total}人中 {start} - {end}人表示中</b>"

        query = app.session.query(model_class)
        if filters is not None:
            query = query.filter(filters)

        total = query.count()
        record_name = model_class.__table__.name
        pagination = Pagination(page=page, display_msg=msg, per_page=PER_PAGE, total=total, record_name=record_name)

        return pagination

    @cache.memoize()
    def get_offset(page):
        return PER_PAGE * (page-1)

    def get_page():
        return request.args.get(get_page_parameter(), type=int, default=1)

    # Common rendering function
    def render_fake_quote_page(fake_quote):
        prev_fake_quote_id = get_prev_fake_quote(fake_quote)
        next_fake_quote_id = get_next_fake_quote(fake_quote)

        return render_template('quote.html',
            fake_quote=fake_quote,
            twitter_share=get_twitter_share_info(fake_quote),
            profile_image_idx=get_profile_image_idx(),
            prev_fake_quote_id=prev_fake_quote_id,
            next_fake_quote_id=next_fake_quote_id,
        )

    def get_next_fake_quote(current_fake_quote):
        next_quote = app.session.query(models.FakeQuote) \
            .filter(models.FakeQuote.id!=current_fake_quote.id) \
            .filter(models.FakeQuote.text > current_fake_quote.text) \
            .order_by(models.FakeQuote.text) \
            .first()

        return next_quote.id if next_quote is not None else None

    def get_prev_fake_quote(current_fake_quote):
        prev_quote = app.session.query(models.FakeQuote) \
            .filter(models.FakeQuote.id!=current_fake_quote.id) \
            .filter(models.FakeQuote.text < current_fake_quote.text) \
            .order_by(models.FakeQuote.text) \
            .first()

        return prev_quote.id if prev_quote is not None else None

    def get_twitter_share_info(fake_quote):
        MAX_LENGTH = 100
        share_url = urllib.parse.quote(
            url_for('show_fake_quote', fake_quote_id=fake_quote.id, _external=True)
        )
        text = '{}\n\n{}『{}』'.format(fake_quote.text, fake_quote.fake_book.fake_author.name, fake_quote.fake_book.title)
        if len(text) >= MAX_LENGTH:
            text  = text[:MAX_LENGTH] + '...'

        share_text = urllib.parse.quote(text)
        return {
            'url': share_url,
            'text': share_text
        }

    def get_profile_image_idx():
        MAX_PROFILE_INDEX = 2
        request_profile = request.args.get('profile', 0)
        try:
            idx = int(request_profile)
        except ValueError:
            idx = 0
        return MAX_PROFILE_INDEX if idx > MAX_PROFILE_INDEX else idx




    # JSON API
    # @app.route('/ese_meigen/<fake_quote_id>/next_json')
    def show_next_fake_quote_json(fake_quote_id):
        # When invalid id is passed, just redirect to random page
        if not util.is_uuid(fake_quote_id):
            return redirect(url_for('show_random_quote'))

        res = app.session.query(
            models.FakeQuote,
            models.FakeBook,
            models.FakeAuthor,
            models.Quote,
            models.Book,
            models.Author
        ) \
        .join(models.FakeQuote.fake_book) \
        .join(models.FakeBook.fake_author) \
        .join(models.FakeQuote.original_quote) \
        .join(models.FakeBook.original_book) \
        .join(models.FakeAuthor.original_author) \
        .filter(models.FakeQuote.id!=fake_quote_id) \
        .first()

        fq, fb, fa, oq, ob, oa = res

        return jsonify(
            test=1,
            fake_quote1=util.model_to_json(fa)
            # fake_quote2=util.model_dict_to_json(next_fake_quote2.to_dict())
        )



    # Unused function. Might prepare JSON API for Ajax
    # @app.route('/ese_meigen/<fake_quote_id>/next_json')
    def show_next_fake_quote_json(fake_quote_id):
        # When invalid id is passed, just redirect to random page
        if not util.is_uuid(fake_quote_id):
            return redirect(url_for('show_random_quote'))

        # TODO: This next is not deterministic
        next_fake_quote = app.session.query(models.FakeQuote) \
        .join(models.FakeBook) \
        .filter(models.FakeQuote.id!=fake_quote_id) \
        .first()

        # next_fake_quote = app.session.query(models.FakeQuote) \
        # .filter(models.FakeQuote.id!=fake_quote_id) \
        # .first()
        print('next_fake_quote')
        print(next_fake_quote)

        print('prev', fake_quote_id)
        print('next', next_fake_quote.id)
        if next_fake_quote == None:
            return redirect(url_for('show_random_quote'))

        next_fake_quote_dict = next_fake_quote.to_dict()
        next_fake_quote_dict['fake_book'] = next_fake_quote.fake_book.to_dict()
        next_fake_quote_dict['fake_book']['fake_author'] = next_fake_quote.fake_book.fake_author.to_dict()

        next_original_quote_dict = next_fake_quote.original_quote.to_dict()
        next_original_quote_dict['book'] = next_fake_quote.original_quote.book.to_dict()
        next_original_quote_dict['book']['author'] = next_fake_quote.original_quote.book.author.to_dict()

        return jsonify(
            fake_quote=util.model_dict_to_json(next_fake_quote_dict),
            twitter_share=get_twitter_share_info(next_fake_quote),
            prev_quiote_id=fake_quote_id
        )

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()


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
from web.models import *

PER_PAGE = 12
CHILDREN_LIMIT = 3

TOP_QUOTE_ID = '2d12dcf4-3bae-418b-8005-aa550c76730c'

def create_app():
    Base.metadata.create_all(bind=engine)
    util.load_env()

    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
    app.json_encoder = util.AppModelEncoder

    cache = Cache(app)

    @app.route('/')
    def show_top():
        TOP_AUTHORS_LIMIT = 4
        fake_quote = app.session.query(FakeQuote).filter_by(id=TOP_QUOTE_ID).first()

        authors = app.session.query(Author) \
            .order_by(func.random()) \
            .limit(TOP_AUTHORS_LIMIT) \
            .all()

        for author in authors:
            books = app.session.query(Book) \
                .filter(Book.author_id==author.id) \
                .order_by(Book.title) \
                .limit(CHILDREN_LIMIT) \
                .all()
            setattr(author, 'books', books)

            book_count = app.session.query(Book) \
                .filter(Book.author_id==author.id) \
                .count()
            setattr(author, 'book_count', book_count)

        return render_template('top.html',
            fake_quote=fake_quote,
            authors=authors
        )

    @app.route('/fake_quotes/random/')
    def show_random_quote():
        # Pick Random Fake Quote
        fake_quote = app.session.query(FakeQuote).order_by(func.random()).first()
        # return render_fake_quote_page(fake_quote)
        return redirect(url_for('show_fake_quote',
            fake_quote_id=fake_quote.id,
            profile=request.args.get('profile', 0)
        ))

    @app.route('/fake_quotes/<fake_quote_id>')
    @cache.cached(query_string=True)
    def show_fake_quote(fake_quote_id):
        # When invalid id is passed, just redirect to random page
        if not util.is_uuid(fake_quote_id):
            return redirect(url_for('show_random_quote'))

        fake_quote = app.session.query(FakeQuote).filter(FakeQuote.id==fake_quote_id).first()
        if fake_quote == None:
            return redirect(url_for('show_random_quote'))

        return render_fake_quote_page(fake_quote)

    @app.route('/original_authors')
    @cache.cached(query_string=True)
    def list_authors():
        page = get_page()
        offset = get_offset(page)

        authors = app.session.query(Author) \
            .order_by(Author.name_kana) \
            .offset(offset) \
            .limit(PER_PAGE) \
            .all()

        for author in authors:
            books = app.session.query(Book) \
                .filter(Book.author_id==author.id) \
                .order_by(Book.title) \
                .limit(CHILDREN_LIMIT) \
                .all()
            setattr(author, 'books', books)

            book_count = app.session.query(Book) \
                .filter(Book.author_id==author.id) \
                .count()
            setattr(author, 'book_count', book_count)


        pagination = get_pagenate(page, Author)
        return render_template('original_author_list.html', authors=authors, pagination=pagination)

    @app.route('/fake_authors')
    @cache.cached(query_string=True)
    def list_fake_authors():
        page = get_page()
        offset = get_offset(page)

        fake_authors = app.session.query(FakeAuthor) \
            .order_by(FakeAuthor.name) \
            .offset(offset) \
            .limit(PER_PAGE) \
            .all()
        return render_fake_author_book_list(page, '', fake_authors)

    def render_fake_author_book_list(page, author, fake_authors, query_filter=None):
        for fake_author in fake_authors:
            fake_books = app.session.query(FakeBook) \
                .filter(FakeBook.fake_author_id==fake_author.id) \
                .order_by(FakeBook.title) \
                .limit(CHILDREN_LIMIT) \
                .all()
            setattr(fake_author, 'fake_books', fake_books)

            fake_book_count = app.session.query(FakeBook) \
                .filter(FakeBook.fake_author_id==fake_author.id) \
                .count()
            setattr(fake_author, 'fake_book_count', fake_book_count)

        pagination = get_pagenate(page, FakeAuthor, query_filter)
        return render_template('fake_list.html', fake_authors=fake_authors, author=author, pagination=pagination)


    @app.route('/original_quotes/<quote_id>/fake_quotes')
    def list_fake_quotes_by_quote(quote_id):
        page = get_page()
        offset = get_offset(page)

        # When invalid id is passed, just redirect to random page
        if not util.is_uuid(quote_id):
            return redirect(url_for('show_random_quote'))

        quote = app.session.query(Quote) \
            .filter(Quote.id==quote_id) \
            .first()

        if quote == None:
            return redirect(url_for('show_random_quote'))

        query_filter = (FakeQuote.quote_id==quote_id)
        fake_quotes = app.session.query(FakeQuote) \
            .filter(query_filter) \
            .order_by(FakeQuote.text) \
            .offset(offset) \
            .limit(PER_PAGE) \
            .all()

        pagination = get_pagenate(page, FakeQuote, query_filter)

        return render_template('fake_quote_list.html', quote=quote, fake_quotes=fake_quotes, pagination=pagination)

    @app.route('/original_authors/<author_name>/fake_authors')
    @cache.cached(query_string=True)
    def list_all_fake_books(author_name):
        page = get_page()
        offset = get_offset(page)

        author = app.session.query(Author).filter_by(name=author_name).first()
        if author == None:
            flash(random_not_found_message(author_name))
            return abort(404)

        fake_authors = app.session.query(FakeAuthor) \
            .filter(FakeAuthor.author_id==author.id) \
            .order_by(FakeAuthor.name) \
            .offset(offset) \
            .limit(PER_PAGE) \
            .all()

        query_filter = (FakeAuthor.author_id==author.id)
        return render_fake_author_book_list(page, author, fake_authors, query_filter)

    @app.route('/fake_authors/<fake_author_name>/fake_books')
    @cache.cached(query_string=True)
    def list_fake_books(fake_author_name):
        fake_author = app.session.query(FakeAuthor).filter_by(name=fake_author_name).first()
        if fake_author == None:
            flash(random_not_found_message(fake_author_name))
            return abort(404)

        page = page = get_page()
        offset = get_offset(page)
        query_filter = (FakeBook.fake_author_id==fake_author.id)

        # .order_by(asc(collate(FakeBook.title, 'ja-x-icu'))) \
        fake_books = app.session.query(FakeBook) \
            .filter(query_filter) \
            .order_by(FakeBook.title) \
            .offset(offset) \
            .limit(PER_PAGE) \
            .all()

        pagination = get_pagenate(page, FakeBook, query_filter)
        return render_template('fake_book_list.html', fake_author=fake_author, fake_books=fake_books, pagination=pagination)


# http://127.0.0.1:5000/books/74969e90-f19b-4d48-8857-e8cc94496c0c/fake_books
    @app.route('/books/<book_id>/quotes')
    @cache.cached(query_string=True)
    def list_quotes_by_book(book_id):
        if not util.is_uuid(book_id):
            return redirect(url_for('show_random_quote'))

        book = app.session.query(Book) \
            .filter_by(id=book_id).first()

        if book == None:
            return redirect(url_for('show_random_quote'))

        page = page = get_page()
        offset = get_offset(page)
        query_filter = (Quote.book_id==book_id)

        quotes = app.session.query(Quote) \
            .filter(query_filter) \
            .order_by(Quote.text) \
            .offset(offset) \
            .limit(PER_PAGE) \
            .all()

        pagination = get_pagenate(page, Quote, query_filter)
        return render_template('quote_list.html', book=book, quotes=quotes, pagination=pagination)

    # @app.errorhandler(404)
    # def not_found(e):
    #     return render_template('404.html')

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
        # prev_fake_quote_id = get_prev_fake_quote(fake_quote)
        # next_fake_quote_id = get_next_fake_quote(fake_quote)
        prev_fake_quote_id = None
        next_fake_quote_id = None

        return render_template('quote.html',
            fake_quote=fake_quote,
            twitter_share=get_twitter_share_info(fake_quote),
            profile_image_idx=get_profile_image_idx(),
            prev_fake_quote_id=prev_fake_quote_id,
            next_fake_quote_id=next_fake_quote_id,
        )

    # def get_next_fake_quote(current_fake_quote):
    #     next_quote = app.session.query(FakeQuote) \
    #         .filter(FakeQuote.id!=current_fake_quote.id) \
    #         .filter(FakeQuote.text > current_fake_quote.text) \
    #         .order_by(FakeQuote.text) \
    #         .first()

    #     return next_quote.id if next_quote is not None else None

    # def get_prev_fake_quote(current_fake_quote):
    #     prev_quote = app.session.query(FakeQuote) \
    #         .filter(FakeQuote.id!=current_fake_quote.id) \
    #         .filter(FakeQuote.text < current_fake_quote.text) \
    #         .order_by(FakeQuote.text) \
    #         .first()

    #     return prev_quote.id if prev_quote is not None else None

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


    #####################
    # JSON API
    #####################
    @app.route('/api/fake_quotes/random')
    def api_random_fake_quotes():
        fake_quote = app.session.query(FakeQuote).order_by(func.random()).first()
        return jsonify(
            fake_quote=fake_quote.to_dict()
        )

    # Id List
    @app.route('/api/authors/id_list')
    @cache.cached(query_string=True)
    def api_authors_id_list():
        return json_res_id_list(Author, Author.name_kana)

    @app.route('/api/books/id_list')
    @cache.cached(query_string=True)
    def api_books_id_list():
        return json_res_id_list(Book, Book.title)

    @app.route('/api/quotes/id_list')
    @cache.cached(query_string=True)
    def api_quotes_id_list():
        return json_res_id_list(Quote, Quote.text)

    @app.route('/api/fake_authors/id_list')
    @cache.cached(query_string=True)
    def api_fake_authors_id_list():
        return json_res_id_list(FakeAuthor, FakeAuthor.name)

    @app.route('/api/fake_books/id_list')
    @cache.cached(query_string=True)
    def api_fake_books_id_list():
        return json_res_id_list(FakeBook, FakeBook.title)

    @app.route('/api/fake_quotes/id_list')
    @cache.cached(query_string=True)
    def api_fake_quotes_id_list():
        return json_res_id_list(FakeQuote, FakeQuote.text)

    # List
    @app.route('/api/authors/list')
    @cache.cached(query_string=True)
    def api_authors_list():
        return jsonify(get_model_dict_list(Author, Author.name_kana))

    @app.route('/api/fake_authors/list')
    @cache.cached(query_string=True)
    def api_fake_authors_list():
        return jsonify(get_model_dict_list(FakeAuthor, FakeAuthor.name))

    # Get by ID
    @app.route('/api/fake_quotes/<fake_quote_id>')

    def api_fake_quote_by_id(fake_quote_id):
        print(fake_quote_id)
        print("fake_quote_id")
        if not util.is_uuid(fake_quote_id):
            print('Not')

            return abort(404)

        fake_quote = app.session.query(FakeQuote).filter(FakeQuote.id==fake_quote_id).first()
        print("fake_quote")
        print(fake_quote)
        if fake_quote == None:
            return abort(404)
        quote = fake_quote.original_quote
        return jsonify(
            fake_quote=fake_quote.to_dict(),
            fake_book=fake_quote.fake_book.to_dict(),
            fake_author=fake_quote.fake_book.fake_author.to_dict(),

            quote=quote.to_dict(),
            book=quote.book.to_dict(),
            author=quote.book.author.to_dict()
        )

    @app.route('/api/authors/<author_id>')
    def api_author_by_id(author_id):
        print(author_id)
        print("author_id")
        if not util.is_uuid(author_id):
            print('Not')
            return abort(404)

        author = app.session.query(Author).filter(Author.id==author_id).first()
        print("author")
        print(author)
        if author == None:
            return abort(404)

        return jsonify(
            author=author.to_dict()
        )

    # // For testing
    @app.route('/api/quotes/<quote_id>')
    def api_quote_by_id(quote_id):
        if not util.is_uuid(quote_id):
            print('Not')
            return abort(404)

        quote = app.session.query(Quote).filter(Quote.id==quote_id).first()

        if quote == None:
            return abort(404)

        return jsonify(
            quote=quote.to_dict()
        )


    def json_res_list(model, order_field, filters=None, only_id=False):
        return jsonify(get_model_dict_list(model, order_field, filters, only_id))
    def get_model_dict_list(model, order_field, filters=None, only_id=False):
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 10))
        query = app.session.query(model)
        if filters is not None:
            query = query.filter(filters)

        m_list = query.order_by(order_field) \
            .limit(limit) \
            .offset(offset) \
            .all()

        # next_offset = offset + limit
        next_offset = -1
        if m_list != None and len(m_list) < limit:
            next_offset = -1

        result_list = []
        if only_id:
            result_list = [m.to_dict()['id'] for m in m_list]
        else:
            result_list = [m.to_dict() for m in m_list]

        return {
            'result_list': result_list,
            'total': total_count(model, filters),
            'next_offset': next_offset
        }

    @cache.memoize()
    def total_count(model, filters):
        query = app.session.query(model)
        if filters is not None:
            query = query.filter(filters)
        return query.count()

    def json_res_id_list(model, order_field):
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 10))
        m_list = app.session.query(model) \
            .order_by(order_field) \
            .limit(limit) \
            .offset(offset) \
            .all()

        # next_offset = offset + limit
        next_offset = -1
        if m_list != None and len(m_list) < limit:
            next_offset = -1

        id_list = [m.to_dict()['id'] for m in m_list]
        return jsonify(
            id_list=id_list,
            next_offset=next_offset
        )

    # ###########
    # Children List
    @app.route('/api/authors/<author_id>/fake_authors/list')
    @cache.cached(query_string=True)
    def api_fake_authors_by_author_id(author_id):
        if not util.is_uuid(author_id):
            print('Not')
            return abort(404)

        author = app.session.query(Author).filter(Author.id==author_id).first()
        print("author")
        print(author)
        if author == None:
            return abort(404)

        # Use pager per FakeAuthor
        filters = (FakeAuthor.author_id==author_id)
        fake_author_list_result = get_model_dict_list(FakeAuthor, FakeAuthor.name, filters)

        return jsonify(
            author=author.to_dict(),
            book_list=[book.to_dict() for book in author.books],
            # fake_author_list=fake_author_list_result['result_list'],
            # fake_author_total=fake_author_list_result['total'],
            # fake_author_next_offset=fake_author_list_result['next_offset']

            children_list=fake_author_list_result['result_list'],
            children_total=fake_author_list_result['total'],
            children_next_offset=fake_author_list_result['next_offset']
        )
# /api/fake_authors/204499f0-b836-4d79-9644-e9454b8f0fb2/fake_books/lis
    @app.route('/api/fake_authors/<fake_author_id>/fake_books/list')
    @cache.cached(query_string=True)
    def api_fake_authors_by_fake_author_id(fake_author_id):
        if not util.is_uuid(fake_author_id):
            print('Not')
            return abort(404)

        fake_author = app.session.query(FakeAuthor).filter(FakeAuthor.id==fake_author_id).first()
        if fake_author == None:
            return abort(404)

        # Use pager per FakeBook
        filters = (FakeBook.fake_author_id==fake_author_id)
        fake_book_list_result = get_model_dict_list(FakeBook, FakeBook.title, filters)

        return jsonify(
            fake_author=fake_author.to_dict(),
            # book_list=[book.to_dict() for book in author.books],
            # fake_author_list=fake_author_list_result['result_list'],
            # fake_author_total=fake_author_list_result['total'],
            # fake_author_next_offset=fake_author_list_result['next_offset']

            children_list=fake_book_list_result['result_list'],
            children_total=fake_book_list_result['total'],
            children_next_offset=fake_book_list_result['next_offset']
        )

    @app.route('/api/books/<book_id>/quotes/list')
    @cache.cached(query_string=True)
    def api_quotes_by_book_id(book_id):
        if not util.is_uuid(book_id):
            return abort(404)

        book = app.session.query(Book).filter(Book.id==book_id).first()
        if book == None:
            return abort(404)

        # Use pager per Quote
        filters = (Quote.book_id==book_id)
        children_list_result = get_model_dict_list(Quote, Quote.text, filters)

        return jsonify(
            book=book.to_dict(),
            children_list=children_list_result['result_list'],
            children_total=children_list_result['total'],
            children_next_offset=children_list_result['next_offset']
        )

    # /http://127.0.0.1:5000/api/quotes/8e7cdd6a-0cf9-446a-9529-57efc7b742fb/fake_quotes/list?offset=0&limit=100
    @app.route('/api/quotes/<quote_id>/fake_quotes/list')
    @cache.cached(query_string=True)
    def api_fake_quotes_by_quote_id(quote_id):
        if not util.is_uuid(quote_id):
            return abort(404)

        quote = app.session.query(Quote).filter(Quote.id==quote_id).first()

        if quote == None:
            return abort(404)

        # Use pager per FakeQuote
        filters = (FakeQuote.quote_id==quote_id)
        children_list_result = get_model_dict_list(FakeQuote, FakeQuote.text, filters)

        return jsonify(
            quote=quote.to_dict(),

            children_list=children_list_result['result_list'],
            children_total=children_list_result['total'],
            children_next_offset=children_list_result['next_offset']
        )

    @app.route('/api/fake_books/<fake_book_id>/fake_quotes/list')
    @cache.cached(query_string=True)
    def api_fake_quotes_by_fake_book_id(fake_book_id):
        if not util.is_uuid(fake_book_id):
            return abort(404)

        fake_book = app.session.query(FakeBook).filter(FakeBook.id==fake_book_id).first()

        if fake_book == None:
            return abort(404)

        # Use pager per FakeQuote
        filters = (FakeQuote.fake_book_id==fake_book_id)
        children_list_result = get_model_dict_list(FakeQuote, FakeQuote.text, filters)

        return jsonify(
            fake_book=fake_book.to_dict(),

            children_list=children_list_result['result_list'],
            children_total=children_list_result['total'],
            children_next_offset=children_list_result['next_offset']
        )

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()


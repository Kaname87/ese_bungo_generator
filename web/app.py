import os
import sys
import random
import urllib.parse

from flask import Flask, request, render_template, redirect, url_for, _app_ctx_stack, abort, flash, jsonify
# from flask_caching import Cache
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

    # cache = Cache(app)

    if os.environ['FLASK_ENV'] != 'production':
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
        def show_fake_quote(fake_quote_id):
            # When invalid id is passed, just redirect to random page
            if not util.is_uuid(fake_quote_id):
                return redirect(url_for('show_random_quote'))

            fake_quote = app.session.query(FakeQuote).filter(FakeQuote.id==fake_quote_id).first()
            if fake_quote == None:
                return redirect(url_for('show_random_quote'))

            return render_fake_quote_page(fake_quote)

        @app.route('/original_authors')
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


        @app.route('/books/<book_id>/quotes')
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

    # if os.environ['FLASK_ENV'] == 'production':
    #     @app.errorhandler(Exception)
    #     def handle_exception(e):
    #         print(e)
    #         app.session.rollback()
    #         return render_template('500.html')

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

    def get_pagenate(page, model_class, filters=None):
        msg = " " # "全{total}人中 {start} - {end}人表示中</b>"

        query = app.session.query(model_class)
        if filters is not None:
            query = query.filter(filters)

        total = query.count()
        record_name = model_class.__table__.name
        pagination = Pagination(page=page, display_msg=msg, per_page=PER_PAGE, total=total, record_name=record_name)

        return pagination

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
        query = app.session.query(FakeQuote.id)

        # If fake_quote_id is passed, get another one
        fake_quote_id = request.args.get('fake_quote_id', None)
        if fake_quote_id is not None and util.is_uuid(fake_quote_id):
            query = query.filter(FakeQuote.id!=fake_quote_id)

        fake_quote = query.order_by(func.random()).first()
        print('fake_quote')
        print(fake_quote.id)
        return api_fake_quote_by_id(str(fake_quote.id))


    # Id List
    @app.route('/api/authors/id_list')
    def api_authors_id_list():
        return json_res_id_list(Author, Author.name_kana)

    @app.route('/api/books/id_list')
    def api_books_id_list():
        return json_res_id_list(Book, Book.title)

    @app.route('/api/quotes/id_list')
    def api_quotes_id_list():
        return json_res_id_list(Quote, Quote.text)

    @app.route('/api/fake_authors/id_list')
    def api_fake_authors_id_list():
        return api_fake_authors_list()
        # return json_res_id_list(FakeAuthor, FakeAuthor.name)

    @app.route('/api/fake_books/id_list')
    def api_fake_books_id_list():
        return json_res_id_list(FakeBook, FakeBook.title)

    @app.route('/api/fake_quotes/id_list')
    def api_fake_quotes_id_list():
        return api_fake_quotes_list()
        # return json_res_id_list(FakeQuote, FakeQuote.text)

    @app.route('/api/fake_quotes/random_id_list')
    def api_fake_quotes_random_id_list():
        order_field = func.random()

                # query = app.session.query(FakeQuote.id)

        # If fake_quote_id is passed, get another one
        filters = None
        fake_quote_id = request.args.get('fake_quote_id', None)
        if fake_quote_id is not None and util.is_uuid(fake_quote_id):
            # query = query.filter()
            filters = (FakeQuote.id!=fake_quote_id)


        return json_res_id_list(FakeQuote, order_field, filters)
    # @app.route('/api/fake_quotes/id_list')
    #     def api_random_fake_quotes_id_list():

    # List
    @app.route('/api/authors/list')
    def api_authors_list():
        # return jsonify(get_model_dict_list(Author, Author.name_kana))
        authors_result = get_model_dict_list(Author, Author.name_kana)
        result = set_children_list(authors_result, Author, Book, Book.title)
        return jsonify(result)


    @app.route('/api/fake_authors/list')
    def api_fake_authors_list():
        fake_authors_result = get_model_dict_list(FakeAuthor, FakeAuthor.name)

        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 10))

        m_list = app.session.query(
                FakeAuthor
            ) \
            .join(Author) \
            .order_by(
                Author.name_kana,
                FakeAuthor.name
            ) \
            .limit(limit) \
            .offset(offset) \
            .all()

        fake_authors_result = {
            'id_list':  [m.to_dict()['id'] for m in m_list],
            'result_list': [m.to_dict() for m in m_list],
            'total': total_count(FakeAuthor, None),
            'next_offset': get_next_offset(offset, limit, m_list)
        }

        result = set_children_list(fake_authors_result, FakeAuthor, FakeBook, FakeBook.title)
        return jsonify(result)

    @app.route('/api/fake_quotes/list')
    def api_fake_quotes_list():

        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 10))

        m_list = app.session.query(
                FakeQuote
            ) \
            .join(FakeBook, FakeQuote.fake_book_id==FakeBook.id) \
            .join(FakeAuthor, FakeBook.fake_author_id==FakeAuthor.id) \
            .join(Quote, FakeQuote.quote_id==Quote.id) \
            .join(Book, Quote.book_id==Book.id) \
            .join(Author, Book.author_id==Author.id) \
            .order_by(
                Author.name_kana,
                Book.title,
                Quote.text,
                FakeAuthor.name,
                FakeBook.title,
                FakeQuote.text
            ) \
            .limit(limit) \
            .offset(offset) \
            .all()

        data = {
            'id_list': [m.to_dict()['id'] for m in m_list],
            'result_list': [m.to_dict() for m in m_list],
            'total': total_count(FakeQuote, None),
            'next_offset': get_next_offset(offset, limit, m_list)
        }

        return jsonify(data)


    def set_children_list(parent_result, Parent, Child, sort_key):

        for parent_dict in parent_result['result_list']:
            parent_filter = (getattr(Child, util.fk_column_name(Parent))==parent_dict['id'])

            children = app.session.query(Child) \
                .filter(parent_filter) \
                .order_by(sort_key) \
                .limit(CHILDREN_LIMIT) \
                .all()


            child_prefex = util.singular_table_name(Child)
            parent_dict[child_prefex + '_list'] = [child.to_dict() for child in children]
            parent_dict[child_prefex + '_total'] = app.session.query(Child).filter(parent_filter).count()

        return parent_result


    # Get by Fake Quote ID. Get all related info
    @app.route('/api/fake_quotes/<fake_quote_id>')

    def api_fake_quote_by_id(fake_quote_id):
        # print(fake_quote_id)
        # print("fake_quote_id")
        if not util.is_uuid(fake_quote_id):
            return abort(404)

        fake_quote = app.session.query(FakeQuote).filter(FakeQuote.id==fake_quote_id).first()
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

    # @app.route('/api/authors/<author_id>')
    # def api_author_by_id(author_id):
    #     print(author_id)
    #     print("author_id")
    #     if not util.is_uuid(author_id):
    #         print('Not')
    #         return abort(404)

    #     author = app.session.query(Author).filter(Author.id==author_id).first()
    #     print("author")
    #     print(author)
    #     if author == None:
    #         return abort(404)

    #     return jsonify(
    #         author=author.to_dict()
    #     )

    # # // For testing
    # @app.route('/api/quotes/<quote_id>')
    # def api_quote_by_id(quote_id):
    #     if not util.is_uuid(quote_id):
    #         print('Not')
    #         return abort(404)

    #     quote = app.session.query(Quote).filter(Quote.id==quote_id).first()

    #     if quote == None:
    #         return abort(404)

    #     return jsonify(
    #         quote=quote.to_dict()
    #     )

    # def json_res_list(model, order_field, filters=None, only_id=False):
    #     return jsonify(get_model_dict_list(model, order_field, filters, only_id))

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

        result_list = []
        if only_id:
            result_list = [m.to_dict()['id'] for m in m_list]
        else:
            result_list = [m.to_dict() for m in m_list]

        return {
            'result_list': result_list,
            'total': total_count(model, filters),
            'next_offset': get_next_offset(offset, limit, m_list)
        }

    def total_count(model, filters):
        query = app.session.query(model)
        if filters is not None:
            query = query.filter(filters)
        return query.count()

    def json_res_id_list(model, order_field, filters=None):
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 10))

        query = app.session.query(model)
        if filters is not None:
            query.filter(filters)

        m_list = query.order_by(order_field) \
            .limit(limit) \
            .offset(offset) \
            .all()

        id_list = [m.to_dict()['id'] for m in m_list]
        return jsonify(
            id_list=id_list,
            next_offset=get_next_offset(offset, limit, m_list)
        )

    def get_next_offset(offset, limit, result):
        next_offset = offset + limit
        if result == None or (result != None and len(result) < limit):
            next_offset = -1

        # Tmp Code for local
        if os.environ['FLASK_ENV'] != 'production':
            next_offset = -1 # TODO: Make this as default for local

        return next_offset

    # ###########
    # Children List
    @app.route('/api/authors/<author_id>/books/list')
    def api_books_by_author_id(author_id):
        result = children_by_parent_id(Author, author_id, Book, Book.title)

        # for fake_author in result['children_list']:
        #     fake_books = app.session.query(FakeBook) \
        #         .filter(FakeBook.fake_author_id==fake_author['id']) \
        #         .order_by(FakeBook.title) \
        #         .limit(CHILDREN_LIMIT) \
        #         .all()
        #     fake_author['fake_book_list'] = [fake_book.to_dict() for fake_book in fake_books]

        # books = app.session.query(Book) \
        #     .filter(Book.author_id==author_id) \
        #     .order_by(Book.title) \
        #     .all()
        # result['book_list'] = [book.to_dict() for book in books]

        return jsonify(result)

    # http://localhost:5000/api/authors/8995788f-77f5-4f5e-a1c3-9dcb9283eac2/fake_authors/list
    @app.route('/api/authors/<author_id>/fake_authors/list')
    def api_fake_authors_by_author_id(author_id):
        result = children_by_parent_id(Author, author_id, FakeAuthor, FakeAuthor.name)

        for fake_author in result['children_list']:
            fake_books = app.session.query(FakeBook) \
                .filter(FakeBook.fake_author_id==fake_author['id']) \
                .order_by(FakeBook.title) \
                .limit(CHILDREN_LIMIT) \
                .all()
            fake_author['fake_book_list'] = [fake_book.to_dict() for fake_book in fake_books]

        books = app.session.query(Book) \
            .filter(Book.author_id==author_id) \
            .order_by(Book.title) \
            .all()
        result['book_list'] = [book.to_dict() for book in books]

        return jsonify(result)

    # /api/fake_authors/204499f0-b836-4d79-9644-e9454b8f0fb2/fake_books/lis
    @app.route('/api/fake_authors/<fake_author_id>/fake_books/list')
    def api_fake_books_by_fake_author_id(fake_author_id):
        result = children_by_parent_id(FakeAuthor, fake_author_id, FakeBook, FakeBook.title)

        # Add Original
        author = app.session.query(Author) \
            .filter(Author.id==result['fake_author']['author_id']) \
            .first()

        result['author'] = author.to_dict()
        result['book_list'] = [book.to_dict() for book in author.books]

        return jsonify(result)

    @app.route('/api/books/<book_id>/quotes/list')
    def api_quotes_by_book_id(book_id):
        result = children_by_parent_id(Book, book_id, Quote, Quote.text)

        # Add Original
        author = app.session.query(Author) \
            .filter(Author.id==result['book']['author_id']) \
            .first()
        result['author'] = author.to_dict()
        return jsonify(result)

    # /http://127.0.0.1:5000/api/quotes/8e7cdd6a-0cf9-446a-9529-57efc7b742fb/fake_quotes/list?offset=0&limit=100
    @app.route('/api/quotes/<quote_id>/fake_quotes/list')
    def api_fake_quotes_by_quote_id(quote_id):
        result = children_by_parent_id(Quote, quote_id, FakeQuote, FakeQuote.text)

        # Add Original
        book = app.session.query(Book) \
            .filter(Book.id==result['quote']['book_id']) \
            .first()
        result['book'] = book.to_dict()
        result['author'] = book.author.to_dict()

        # Add Fake Parent
        for fake_quote in result['children_list']:
            fake_book = app.session.query(FakeBook) \
                .filter(FakeBook.id==fake_quote['fake_book_id']) \
                .first()
            fake_quote['fake_book'] = fake_book.to_dict()
            fake_quote['fake_author'] = fake_book.fake_author.to_dict()

        return jsonify(result)

    @app.route('/api/fake_books/<fake_book_id>/fake_quotes/list')
    def api_fake_quotes_by_fake_book_id(fake_book_id):
        result = children_by_parent_id(FakeBook, fake_book_id, FakeQuote, FakeQuote.text)

        # Add Original
        book = app.session.query(Book) \
            .filter(Book.id==result['fake_book']['book_id']) \
            .first()
        result['book'] = book.to_dict()
        result['author'] = book.author.to_dict()

        # Add Parent
        fake_author = app.session.query(FakeAuthor) \
            .filter(FakeAuthor.id==result['fake_book']['fake_author_id']) \
            .first()
        result['fake_author'] = fake_author.to_dict()

        return jsonify(result)

    def children_by_parent_id(Parent, parent_id, Child, sort_key):
        if not util.is_uuid(parent_id):
            return abort(404)

        parent = app.session.query(Parent).filter(Parent.id==parent_id).first()

        if parent == None:
            return abort(404)

        # Use pager per Child model

        filters = (getattr(Child, util.fk_column_name(Parent))==parent_id)
        children_list_result = get_model_dict_list(Child, sort_key, filters)

        # util.singular(parent.__tablename__)
        child_key_prefix = util.singular_table_name(Child)
        return {
            util.singular_table_name(Parent): parent.to_dict(),
            # child_key_prefix + '_list': children_list_result['result_list'],
            # child_key_prefix + '_total': children_list_result['total'],
            # child_key_prefix + '_next_offset': children_list_result['next_offset'],
            'children_list': children_list_result['result_list'],
            'children_total': children_list_result['total'],
            'children_next_offset': children_list_result['next_offset']
        }


    @app.after_request
    def add_header(response):
        response.headers.add("Access-Control-Allow-Origin", "*")

        return response

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()

#!/usr/bin/python
import const
import psycopg2
import util
# from config import config

def get_connect():
    return psycopg2.connect("dbname=ese_bungo user=kaname")


def select_or_insert_author(cur, author_name, author_name_kana, ):
    cur.execute("SELECT id from authors where name = %s", (author_name, ))

    if cur.rowcount == 0:
        print("Insert new author: {}".format(author_name))
        cur.execute("INSERT INTO authors (name, name_kana) VALUES (%s, %s) RETURNING id", (author_name, author_name_kana))
    # else:
    #     print("Already exiest")

    return cur.fetchone()[0]

def select_or_insert_book(cur, author_id, title, url):
    cur.execute("SELECT id from books where author_id = %s and title = %s",
        (author_id, title))

    if cur.rowcount == 0:
        print("Insert new book: {}".format(title))
        cur.execute("INSERT INTO books  (author_id, title, url) VALUES (%s, %s, %s) RETURNING id",
            (author_id, title, url))
    # else:
    #     print("Already exiest")

    return cur.fetchone()[0]

def select_or_insert_quote(cur, book_id, text):
    cur.execute("SELECT id from quotes where book_id = %s and text = %s",
        (book_id, text))

    if cur.rowcount == 0:
        print("Insert new quote: {}".format(text))
        cur.execute("INSERT INTO quotes (book_id, text) VALUES (%s, %s) RETURNING id",
            (book_id, text))
    # else:
    #     print("Already exiest")

    return cur.fetchone()[0]

def import_data(src = const.ORIGINAL_NOVEL_SOURCE):
    conn = None
    try:
        conn = get_connect()
        cur = conn.cursor()

        source_dict = util.read_json_to_dict(src)
        print(source_dict)
        for author_name, data in source_dict.items():
            print('Procss: {}'.format(author_name))
            author_id = select_or_insert_author(cur, author_name, data['author']['name_kana'])
            for book in data['novels']:
                book_id = select_or_insert_book(cur, author_id, book.get('title'), book.get('url'))
                for quote_text in book['quotes']:
                    quote_id = select_or_insert_quote(cur, book_id, quote_text)

        cur.close()

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    # import_data()
    # print(11111)
    import_data()
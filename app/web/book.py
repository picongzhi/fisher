import json

from flask import jsonify, request

from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from . import web
from app.forms.book import SearchForm
from app.view_models.book import BookViewModel, BookCollection


@web.route('/book/search')
def search():
    """
    :param q: 搜索关键字或isbn
    :param page:
    :return:
    """
    # isbn13 13个0~9的数字组成
    # isbn10 10个0~9的数组组成，包含-
    form = SearchForm(request.args)
    books = BookCollection()

    if not form.validate():
        return jsonify(form.errors)

    q = form.q.data.strip()
    page = form.page.data
    isbn_or_key = is_isbn_or_key(q)

    yushu_book = YuShuBook()
    if isbn_or_key == 'isbn':
        yushu_book.search_by_isbn(q)
    else:
        yushu_book.search_by_keyword(q, page)
    books.fill(yushu_book, q)

    # return jsonify(books.__dict__)
    return json.dumps(books, default=lambda o: o.__dict__)

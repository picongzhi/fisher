import json

from flask import jsonify, request, render_template, flash
from flask_login import current_user

from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from . import web
from app.forms.book import SearchForm
from app.view_models.book import BookViewModel, BookCollection
from app.view_models.trade import TradeInfo
from app.models.wish import Wish
from app.models.gift import Gift


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
        # return jsonify(form.errors)
        flash('搜索的关键字不符合要求，请重新输入关键字')

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
    # return json.dumps(books, default=lambda o: o.__dict__)
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    return render_template('book_detail.html',
                           book=book,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes)

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship
from flask import current_app

from .base import db, Base
from .wish import Wish
from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('user.id'))
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)

        return yushu_book.first

    @classmethod
    def recent(cls):
        return Gift.query.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()

    @classmethod
    def get_user_gifts(cls, uid):
        return Gift.query.filter_by(
            uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()

    @classmethod
    def get_wish_counts(cls, isbn_list):
        count_list = db.session.query(
            func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False, Wish.isbn.in_(isbn_list), Wish.status == 1).group_by(
            Wish.isbn).all()

        return [{'count': w[0], 'isbn': w[1]} for w in count_list]

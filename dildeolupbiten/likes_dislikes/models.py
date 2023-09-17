# -*- coding: utf-8 -*-

from dildeolupbiten import db


class LikeDislike(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class LikeDislikeArticle(LikeDislike):
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"))


class LikeDislikeComment(LikeDislike):
    comment_id = db.Column(db.Integer, db.ForeignKey("comment.id"))

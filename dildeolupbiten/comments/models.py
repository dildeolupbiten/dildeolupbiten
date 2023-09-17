# -*- coding: utf-8 -*-

from datetime import datetime as dt

from dildeolupbiten import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    date = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"), nullable=False)
    likes_dislikes = db.relationship("LikeDislikeComment", backref="comment", cascade="all, delete-orphan")
    children = db.relationship("Comment", back_populates="parent")
    parent = db.relationship("Comment", back_populates="children", remote_side=[id])


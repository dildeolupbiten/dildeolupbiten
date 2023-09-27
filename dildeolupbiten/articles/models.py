# -*- coding: utf-8 -*-

from datetime import datetime as dt

from dildeolupbiten import db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
    image = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship("Comment", backref="article", cascade="all, delete-orphan")
    likes_dislikes = db.relationship("LikeDislikeArticle", backref="article", cascade="all, delete-orphan")

# -*- coding: utf-8 -*-

from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer, SignatureExpired, BadSignature

from dildeolupbiten import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    image = db.Column(db.String(255), default="default.png")
    articles = db.relationship("Article", backref="user", cascade="all, delete-orphan")
    comments = db.relationship("Comment", backref="user", cascade="all, delete-orphan")
    like_dislike_articles = db.relationship("LikeDislikeArticle", backref="user", cascade="all, delete-orphan")
    like_dislike_comments = db.relationship("LikeDislikeComment", backref="user", cascade="all, delete-orphan")

    def get_reset_token(self):
        s = Serializer(current_app.config["SECRET_KEY"])
        return s.dumps({"user_id": self.id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except (SignatureExpired, BadSignature):
            return None
        return User.query.get(user_id)

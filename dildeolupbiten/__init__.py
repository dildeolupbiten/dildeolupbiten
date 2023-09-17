# -*- coding: utf-8 -*-

from flask import Flask
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


def create_app():
    from dildeolupbiten.config import Config
    from dildeolupbiten.main.routes import main
    from dildeolupbiten.users.routes import users
    from dildeolupbiten.articles.routes import articles
    import dildeolupbiten.users.models
    import dildeolupbiten.articles.models
    import dildeolupbiten.comments.models
    import dildeolupbiten.likes_dislikes.models
    from dildeolupbiten.utils import render, count_attr, search_article, orphan_comments
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(users)
    app.register_blueprint(articles)
    app.register_blueprint(main)
    app.jinja_env.globals.update(str=str)
    app.jinja_env.globals.update(isinstance=isinstance)
    app.jinja_env.globals.update(list=list)
    app.jinja_env.globals.update(len=len)
    app.jinja_env.globals.update(zip=zip)
    app.jinja_env.globals.update(enumerate=enumerate)
    app.jinja_env.globals.update(render=render)
    app.jinja_env.globals.update(count_attr=count_attr)
    app.jinja_env.globals.update(search_article=search_article)
    app.jinja_env.globals.update(orphan_comments=orphan_comments)
    with app.app_context():
        db.init_app(app)
        # db.drop_all()
        db.create_all()
        bcrypt.init_app(app)
        login_manager.init_app(app)
        mail.init_app(app)
    return app

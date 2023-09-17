# -*- coding: utf-8 -*-

from flask import render_template, Blueprint, request

from dildeolupbiten.articles.models import Article

main = Blueprint("main", __name__)


@main.route("/home")
@main.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    articles = Article.query.order_by(Article.date.desc()).paginate(page=page, per_page=3)
    return render_template('main/home.html', articles=articles, title="Home")


@main.route("/about")
def about():
    return render_template("main/about.html", title='About')

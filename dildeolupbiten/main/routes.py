# -*- coding: utf-8 -*-

from flask import render_template, Blueprint, request, url_for, json, Response

from dildeolupbiten.articles.models import Article
from dildeolupbiten.utils import get_all_articles

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def view():
    articles = get_all_articles()
    if "articles" in request.form:
        return Response(json.dumps(articles), 200)
    return render_template('main/view.html', articles=json.dumps(articles))


@main.route("/all_articles", methods=["GET", "POST"])
def all_articles():
    articles = get_all_articles()
    if "articles" in request.form:
        return Response(json.dumps(articles), 200)
    return render_template('main/list.html', articles=json.dumps(articles), title="Browse All Articles")


@main.route("/about")
def about():
    return render_template("main/about.html", title='About')

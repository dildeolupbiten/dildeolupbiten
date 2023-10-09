# -*- coding: utf-8 -*-

from flask import render_template, Blueprint, request, json, Response, url_for
from dildeolupbiten.utils import get_all_articles, get_categories

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def view():
    articles = get_all_articles()[:6]
    if "articles" in request.form:
        return Response(json.dumps(articles), 200)
    return render_template(
        'main/view.html',
        title="Home",
        exists=len(articles),
        href=url_for("main.all_articles"),
        innerHTML="Browse All Articles"
    )


@main.route("/all_articles", methods=["GET", "POST"])
def all_articles():
    if "all_articles" in request.form:
        return Response(json.dumps(articles = get_all_articles()), 200)
    return render_template('main/list.html', title="All Articles")


@main.route("/categories", methods=["GET", "POST"])
def categories():
    if "categories" in request.form:
        return Response(json.dumps(get_categories(get_all_articles())), 200)
    return render_template("main/categories.html", title='Categories')


@main.route("/about")
def about():
    return render_template("main/about.html", title='About')

# -*- coding: utf-8 -*-

from flask import render_template, Blueprint, request, url_for, json, Response

from dildeolupbiten.articles.models import Article

main = Blueprint("main", __name__)


@main.route("/home", methods=["GET", "POST"])
@main.route("/", methods=["GET", "POST"])
def home():
    articles = Article.query.order_by(Article.date.desc())
    articles = [
        {
            "title": article.title,
            "description": article.description,
            "article_img": url_for("static", filename="images/" + article.image),
            "article_href": url_for("articles.article", article_title=article.title),
            "date": article.date.strftime('%b %d, %Y').replace(" 0", " "),
            "author_img": url_for("static", filename="images/" + article.user.image),
            "author_href": url_for("users.user_articles", username=article.user.username),
            "author_name": article.user.username

        } for article in articles
    ]
    if "articles" in request.form:
        return Response(json.dumps(articles), 200)
    return render_template('main/home.html', articles=json.dumps(articles), title="Home")


@main.route("/about")
def about():
    return render_template("main/about.html", title='About')

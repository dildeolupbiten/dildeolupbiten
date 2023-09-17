# -*- coding: utf-8 -*-

import sqlalchemy.exc

from flask_login import current_user, login_required
from flask import redirect, url_for, request, flash, render_template, abort, Blueprint, Response, json

from dildeolupbiten import db
from dildeolupbiten.articles.models import Article
from dildeolupbiten.articles.forms import ArticleForm, ArticleUpdateForm
from dildeolupbiten.utils import (
    save_image, response_children, add_comment, delete_comment, update_comment, like_dislike_comment
)

articles = Blueprint("articles", __name__)


@articles.route("/article/create", methods=["GET", "POST"])
@login_required
def create():
    form = ArticleForm()
    response = None
    if form.validate_on_submit():
        a = Article(
            title=form.title.data,
            description=form.description.data,
            content=form.content.data,
            user=current_user,
            image=save_image(form, request.files["image"], (600, 200))
        )
        db.session.add(a)
        try:
            db.session.commit()
            flash("Article created successfully.", "success")
            return redirect(url_for("articles.article", article_title=form.title.data))
        except sqlalchemy.exc.IntegrityError:
            flash("There is an article using this title, change the title of the article.", "danger")
            return redirect(url_for("articles.create"))
    return render_template(
        "articles/create.html",
        title="Create Article",
        form=form,
        columns=[form.title, form.description, form.content, form.image],
        names=["title", "description", "content", "image"],
        response=response
    )


@articles.route("/article/<string:article_title>", methods=["GET", "POST"])
def article(article_title):
    a = Article.query.filter_by(title=article_title).first_or_404()
    if "comments" in request.form:
        return response_children(a, request.url_root)
    if request.method == "POST":
        if current_user.is_authenticated:
            if "add" in request.form:
                return add_comment(request, db, a,)
            elif "delete" in request.form:
                return delete_comment(request, db, a)
            elif "update" in request.form:
                return update_comment(request, db)
            elif "like_dislike" in request.form:
                return like_dislike_comment(request, db, a)
        else:
            return Response("", 404)
    if request.method == "GET":
        if a:
            data = {"title": a.title}
        else:
            data = {"title": None}
        Response(json.dumps(data), 201)
    return render_template(
        "articles/article.html",
        title=a.title,
        articles=[a],
        current_user=current_user,
        primary_id=a.id
    )


@articles.route("/article/<string:article_title>/update", methods=["GET", "POST"])
@login_required
def update(article_title):
    a = Article.query.filter_by(title=article_title).first_or_404()
    if a.user != current_user:
        abort(403)
    form = ArticleUpdateForm()
    if form.validate_on_submit():
        if form.image.data:
            a.image = save_image(form, request.files["image"], (600, 200))
        a.title = form.title.data
        a.content = form.content.data
        a.description = form.description.data
        db.session.commit()
        flash("Article has been updated!", "success")
        return redirect(url_for("articles.article", article_title=a.title))
    elif request.method == "GET":
        form.title.data = a.title
        form.content.data = a.content
        form.description.data = a.description
        form.image.data = a.image
    return render_template(
        "articles/create.html",
        title="Update Article",
        form=form,
        columns=[form.title, form.description, form.content, form.image],
        names=["title", "description", "content", "image"]
    )


@articles.route("/article/<string:article_title>/delete", methods=["GET"])
@login_required
def delete_article(article_title):
    a = Article.query.filter_by(title=article_title).first_or_404()
    if a.user != current_user:
        abort(403)
    db.session.delete(a)
    db.session.commit()
    flash("Article has been deleted.", "success")
    return redirect(url_for("main.home"))

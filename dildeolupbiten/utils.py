# -*- coding: utf-8 -*-

import re
import os

from markdown import markdown
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask import current_app, Response, json, url_for, Request
from flask_sqlalchemy import SQLAlchemy

from pygments import highlight
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments.formatters import Terminal256Formatter

from dildeolupbiten.users.models import User
from dildeolupbiten.articles.models import Article
from dildeolupbiten.comments.models import Comment
from dildeolupbiten.likes_dislikes.models import LikeDislikeArticle, LikeDislikeComment


def api_info(filename, url) -> str | None:
    if not all(isinstance(i, str) for i in [filename, url]):
        return
    if os.path.exists(filename):
        with open(filename, encoding="utf-8") as f:
            return f.read().replace("/api/italian_verbs", url)


def pygmentize(string) -> str | None:
    if not isinstance(string, str):
        return
    return highlight(
        code=string,
        lexer=get_lexer_by_name("markdown"),
        formatter=Terminal256Formatter(style="material")
    )


def count_attr(model, value) -> int | None:
    if any(isinstance(model, i) for i in [Article, Comment]) and isinstance(value, int):
        return len([i for i in model.likes_dislikes if i.value == value])


def orphan_comments(model) -> list | None:
    if isinstance(model, Article):
        return list(filter(lambda i: not i.parent, model.comments))


def find_children_recursively(elements, url_root):
    if not isinstance(elements, list) and not isinstance(url_root, str):
        return
    data = []
    try:
        username = current_user.username
    except AttributeError:
        username = ""
    for i in elements:
        obj = {
            "id": i.id,
            "username": i.user.username,
            "date": i.date.strftime('%b %d, %Y').replace(" 0", " "),
            "src": f"{url_root}static/images/{i.user.image}",
            "href": f"{url_root}user/{i.user.username}",
            "content": HTMLCodeFormat(i.content).highlight(),
            "hidden_value": i.content,
            "likes": count_attr(i, 1),
            "dislikes": count_attr(i, -1),
            "children": [],
            "current_user": username
        }
        if i.children:
            for child in find_children_recursively(list(i.children), url_root):
                obj["children"] += [child]
        data.append(obj)
    return data


def response_children(model, url_root):
    if isinstance(model, Article) and isinstance(url_root, str):
        data = find_children_recursively(orphan_comments(model), url_root)
        return Response(json.dumps(data), 200)


def add_comment(request, db, article):
    if not isinstance(request, Request) or not isinstance(db, SQLAlchemy) or not isinstance(article, Article):
        return
    ids = request.form["primary_id"].split("-")
    content = HTMLCodeFormat(request.form["content"]).highlight()
    hidden_value = request.form["content"]
    if len(ids) == 2:
        comment = Comment(
            content=hidden_value,
            user=current_user,
            article=article
        )
        db.session.add(comment)
        db.session.commit()
        data = {
            "primary_id": request.form["primary_id"],
            "secondary_id": comment.id,
            "content": content,
            "hidden_value": hidden_value,
            "total": len(list(filter(lambda i: not i.parent, article.comments))),
            "username": current_user.username,
            "date": comment.date.strftime('%b %d, %Y').replace(" 0", " "),
            "src": f"{request.url_root}static/images/{current_user.image}",
            "href": f"{request.url_root}user/{current_user.username}",
            "likes": 0,
            "dislikes": 0,
            "children": []
        }
        return Response(json.dumps(data), 200)
    else:
        parent = Comment.query.filter_by(id=ids[-1]).first_or_404()
        comment = Comment(
            content=hidden_value,
            user=current_user,
            parent=parent,
            article=article
        )
        db.session.add(comment)
        db.session.commit()
        data = {
            "primary_id": request.form["primary_id"],
            "secondary_id": comment.id,
            "content": content,
            "hidden_value": hidden_value,
            "total": len(list(parent.children)),
            "likes": 0,
            "dislikes": 0,
            "children": [],
            "username": current_user.username,
            "date": comment.date.strftime('%b %d, %Y').replace(" 0", " "),
            "src": f"{request.url_root}static/images/{current_user.image}",
            "href": f"{request.url_root}user/{current_user.username}"
        }
        return Response(json.dumps(data), 200)


def delete_comment(request, db, article):
    if not isinstance(request, Request) or not isinstance(db, SQLAlchemy) or not isinstance(article, Article):
        return
    ids = request.form["primary_id"].split("-")
    comment = Comment.query.filter_by(id=ids[-1], user=current_user).first_or_404()
    if comment.parent:
        total = len(list(comment.parent.children))
    else:
        total = len(list(filter(lambda i: not i.parent, article.comments)))
    db.session.delete(comment)
    db.session.commit()
    data = {
        "primary_id": request.form["primary_id"],
        "parent_id": "-".join(ids[:-1]),
        "total": total - 1
    }
    return Response(json.dumps(data), 200)


def update_comment(request, db):
    ids = request.form["primary_id"].split("-")
    content = HTMLCodeFormat(request.form["content"]).highlight()
    hidden_value = request.form["content"]
    if not hasattr(current_user, "username"):
        return
    comment = Comment.query.filter_by(id=ids[-1], user=current_user).first()
    if not comment:
        return
    comment.content = hidden_value
    db.session.commit()
    data = {
        "primary_id": request.form["primary_id"],
        "content": content,
        "hidden_value": hidden_value
    }
    return Response(json.dumps(data), 200)


def like_dislike_comment(request, db, article):
    if not isinstance(request, Request) or not isinstance(db, SQLAlchemy) or not isinstance(article, Article):
        return
    ids = request.form["primary_id"].split("-")
    value = int(request.form["value"])
    if len(ids) == 2:
        model = article
        select = "article"
        like_dislike = LikeDislikeArticle.query.filter_by(
            user_id=current_user.id, **{select: model}
        ).first()
        if not like_dislike:
            like_dislike = LikeDislikeArticle(
                value=value,
                user=current_user,
                **{select: model}
            )
            db.session.add(like_dislike)
        else:
            if like_dislike.value == value:
                db.session.delete(like_dislike)
            else:
                like_dislike.value = value
    else:
        model = Comment.query.filter_by(id=ids[-1]).first_or_404()
        select = "comment"
        like_dislike = LikeDislikeComment.query.filter_by(
            user_id=current_user.id, **{select: model}
        ).first()
        if not like_dislike:
            like_dislike = LikeDislikeComment(
                value=value,
                user=current_user,
                **{select: model}
            )
            db.session.add(like_dislike)
        else:
            if like_dislike.value == value:
                db.session.delete(like_dislike)
            else:
                like_dislike.value = value
    db.session.commit()
    data = {
        "like": count_attr(model, 1),
        "dislike": count_attr(model, -1),
        "primary_id": request.form["primary_id"]
    }
    return Response(json.dumps(data), 200)


def query(d, keys):
    if not isinstance(d, dict) and not isinstance(keys, list):
        return

    def recursive_query(dct: dict, key: list):
        result = {}
        for k, v in dct.items():
            if isinstance(v, dict):
                sub = recursive_query(v, key)
                if sub:
                    result.update({k: sub})
            if k in key:
                result[k] = v
        return result
    return recursive_query(d, keys)


def get_article_info(article):
    if not isinstance(article, Article):
        return
    return {
        "title": article.title,
        "category": article.category + " / " + article.title,
        "article_img": article.image,
        "article_href": url_for("articles.article", article_title=article.title),
        "date": article.date.strftime('%b %d, %Y').replace(" 0", " "),
        "author_img": url_for("static", filename="images/" + article.user.image),
        "author_href": url_for("users.view", username=article.user.username),
        "author_name": article.user.username
    }


def get_all_articles():
    return [get_article_info(article) for article in Article.query.order_by(Article.date.desc())]


def get_categories(articles):
    d = {}
    for article in articles:
        category = article["category"].split(" / ")
        if category and category[0]:
            if "category" not in d:
                d["category"] = category[0]
                d["children"] = []
            if not d["children"]:
                d["children"].extend(get_categories([{"category": " / ".join(category[1:])}]))
            else:
                categories = get_categories([{"category": " / ".join(category[1:])}])
                control = False
                for i in categories:
                    for j in d["children"]:
                        index = d["children"].index(j)
                        if i["category"] == j["category"]:
                            d["children"][index]["children"].extend(i["children"])
                            control = False
                        else:
                            control = True
                if control:
                    d["children"].extend(categories)
    return [d] if d else []


def get_user_articles(user):
    if not isinstance(user, User):
        return
    return [
        get_article_info(article)
        for article in Article.query.filter_by(user=user).order_by(Article.date.desc())
    ]


def select_image(username):
    if not isinstance(username, str):
        return
    if username == os.environ["BASIC_AUTH_USERNAME"]:
        return "logo.svg"
    for i in os.listdir(current_app.root_path + url_for("static", filename="images/")):
        if i.startswith("letter") and i.endswith(username[0].lower() + ".svg"):
            return i


def permitted(app):
    if not isinstance(app, current_app.__class__):
        return
    with app.app_context():
        return [
            os.environ["BASIC_AUTH_USERNAME"],
            *[i.username for i in User.query.filter_by(permission=True).all()]
        ]


class ViewModel(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == os.environ["BASIC_AUTH_USERNAME"]


class MetaHTMLCodeFormat(type):
    def __call__(cls, text):
        if not isinstance(text, str):
            return
        return super().__call__(cls.reformat(text))

    def reformat(cls, text: str):
        d_container = "<div class=\"container\">\n"
        d_flex = "<div class=\"d-flex\">\n"
        d_rows = "<div class=\"bg-dark pt-2 pl-2 pr-2 rounded-left text-light\">\n"
        d_close = "\n</div>\n"
        d_code = "<div class=\"bg-dark pt-2 pl-2 pr-2 rounded-right container\">\n"
        patterns = re.findall(r'\[code="([^"]*)"](.*?)\[/code]', text, re.DOTALL)
        langs = []
        for code in sorted(set(patterns), key=patterns.index):
            lang, _code = tuple(map(str.strip, code))[:]
            langs.append(lang)
            html = "".join(
                [
                    d_container,
                    d_flex,
                    d_rows,
                    "```\n",
                    *map(lambda i: f"{i + 1}\n", range(len(_code.split("\n")))),
                    "```\n",
                    d_close,
                    d_code,
                    f"```{lang}\n" + _code + "\n```",
                    d_close,
                    d_close,
                    d_close
                ]
            )
            text = text.replace(code[1], html)
            text = text.replace(f"[code=\"{lang}\"]", "").replace("[/code]", "")
        return text


class HTMLCodeFormat(str, metaclass=MetaHTMLCodeFormat):
    def __init__(self, text: str):
        super().__init__()

    def highlight(self, style="github-dark"):
        if style not in get_all_styles():
            return self
        return "".join(
            [
                markdown(self, extensions=["fenced_code", "codehilite"]),
                "<style>",
                HtmlFormatter(style=style, full=True, cssclass="codehilite").get_style_defs(),
                "</style>"
            ]
        )

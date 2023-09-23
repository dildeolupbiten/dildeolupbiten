# -*- coding: utf-8 -*-

import os

from PIL import Image
from markdown import markdown
from flask_login import current_user
from flask import current_app, Response, json

from pygments.formatters.html import HtmlFormatter
from pygments.formatters import Terminal256Formatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments import highlight

from dildeolupbiten.articles.models import Article
from dildeolupbiten.comments.models import Comment
from dildeolupbiten.likes_dislikes.models import LikeDislikeArticle, LikeDislikeComment


def api_info(filename, url):
    with open(filename, encoding="utf-8") as f:
        return f.read().replace("/api/italian_verbs", url)


def save_image(form, file, thumbnail):
    picture_path = os.path.join(current_app.root_path, "static/images", file.filename)
    img = Image.open(form.image.data)
    img.thumbnail(thumbnail)
    img.save(picture_path)
    return file.filename


def render(string):
    return ("{}" * 4).format(
        markdown(string, extensions=["fenced_code", "codehilite"]),
        "<style>",
        HtmlFormatter(style="default", full=True, cssclass="codehilite").get_style_defs(),
        "</style>"
    )


def pygmentize(string):
    return highlight(code=string, lexer=get_lexer_by_name("markdown"), formatter=Terminal256Formatter(style="material"))


def count_attr(model, value):
    return len([i for i in model.likes_dislikes if i.value == value])


def orphan_comments(model):
    return list(filter(lambda i: not i.parent, model.comments))


def search_article(title):
    article = Article.query.filter_by(title=title).first_or_404()
    return article.title


def find_children_recursively(elements, url_root):
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
            "content": render(i.content),
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
    data = find_children_recursively(orphan_comments(model), url_root)
    return Response(json.dumps(data), 200)


def add_comment(request, db, article):
    ids = request.form["primary_id"].split("-")
    content = render(request.form["content"])
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
    content = render(request.form["content"])
    hidden_value = request.form["content"]
    comment = Comment.query.filter_by(id=ids[-1], user=current_user).first_or_404()
    comment.content = hidden_value
    db.session.commit()
    data = {
        "primary_id": request.form["primary_id"],
        "content": content,
        "hidden_value": hidden_value
    }
    return Response(json.dumps(data), 200)


def like_dislike_comment(request, db, article):
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


def query(d: dict, keys: list):
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


def update(d: dict, sub_d: dict):
    for key, value in d.items():
        if key in sub_d:
            for k in sub_d[key]:
                d[key][k].update(sub_d[key][k])
        if isinstance(value, dict):
            update(value, sub_d)
    return d

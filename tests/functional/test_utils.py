# -*- coding: utf-8 -*-

from dildeolupbiten.utils import *
from flask_login import login_user


def test_api_info():
    # Test with an invalid filename.
    assert api_info(1, "<url>", "Italian Verbs") is None
    # Test with the valid filename.
    result = api_info(
        "./dildeolupbiten/api/italian_verbs/italian_verbs.md",
        "<url>",
        "Italian Verbs"
    )
    assert result
    assert "api" in result


def test_pygmentize():
    # Render a not str value
    assert pygmentize(1) is None
    # Render a str value
    assert pygmentize("a")


def test_count_attr(app, client, test_user, test_data):
    with app.test_request_context():
        # Test with invalid arguments
        assert count_attr("a", "b") is None
        # Set the transaction user_id.
        with client.session_transaction() as session_transaction:
            session_transaction['user_id'] = test_user.id
        # Login as test_user.
        login_user(test_user)
        # Create an article with post request
        data = test_data("New")
        response = client.post(
            "/article/create",
            data=data,
            headers={"X-Requested-With": "XMLHttpRequest"}
        )
        assert response.status_code == 302
        article = Article.query.filter_by(title=data["title"]).first()
        assert article
        assert count_attr(article, 1) == 0
        # Like the article
        data = {
            "primary_id": f"New Title-secondary",
            "like_dislike": True,
            "value": 1
        }
        response = client.post(
            "/article/New Title",
            data=data,
            headers={"X-Requested-With": "XMLHttpRequest"}
        )
        assert response.status_code == 200
        # Now let's count the like amount. (Valid for Comment class also)
        assert count_attr(article, 1) == 1
        # Delete the article
        response = client.get("/article/New Title/delete")
        assert response.status_code == 302
        assert "Redirecting" in response.data.decode()
        assert Article.query.filter_by(title="New Title").first() is None


def test_orphan_comments(app, client, test_user, test_data):
    # Test with an invalid argument
    assert orphan_comments("") is None
    # Set the transaction user_id.
    with client.session_transaction() as session_transaction:
        session_transaction['user_id'] = test_user.id
    # Login as test_user.
    login_user(test_user)
    # Create an article with post request
    data = test_data("New")
    response = client.post(
        "/article/create",
        data=data,
        headers={"X-Requested-With": "XMLHttpRequest"}
    )
    assert response.status_code == 302
    article = Article.query.filter_by(title=data["title"]).first()
    assert article
    # Create a comment with post request
    comment_data = {
        "content": "New Content",
        "primary_id": "New-secondary",
        "add": True
    }
    # Send a post request with an unauthorized user.
    response = client.post(
        "/article/New Title",
        data=comment_data,
        headers={"X-Requested-With": "XMLHttpRequest"}
    )
    # Check if the comment exists
    assert response.status_code == 200
    comment = Comment.query.filter_by(content="New Content").first()
    assert comment
    # Not let's assume comment is an orphan comment.
    assert orphan_comments(article) == [comment]
    # Delete the article
    response = client.get("/article/New Title/delete")
    assert response.status_code == 302
    assert "Redirecting" in response.data.decode()
    assert Article.query.filter_by(title="New Title").first() is None


def test_find_children_recursively(app, client, test_user, test_data):
    with app.test_request_context() as ctx:
        # Test with invalid arguments
        assert find_children_recursively("", "") == []
        # Set the transaction user_id.
        with client.session_transaction() as session_transaction:
            session_transaction['user_id'] = test_user.id
        # Login as test_user.
        login_user(test_user)
        # Create an article with post request
        data = test_data("Other")
        response = client.post(
            "/article/create",
            data=data,
            headers={"X-Requested-With": "XMLHttpRequest"}
        )
        assert response.status_code == 302
        article = Article.query.filter_by(title=data["title"]).first()
        assert article
        # Now let's create 10 comments that each one is the child of the previous comment.
        primary_id = "Other Title-secondary"
        comments = []
        for i in range(10):
            # Create a comment with post request
            comment_data = {
                "content": f"Other Content-{i}",
                "primary_id": primary_id,
                "add": True
            }
            # Send a post request with an unauthorized user.
            response = client.post(
                "/article/Other Title",
                data=comment_data,
                headers={"X-Requested-With": "XMLHttpRequest"}
            )
            # Check if the comment exists
            assert response.status_code == 200
            comment = Comment.query.filter_by(content=f"Other Content-{i}").first()
            assert comment
            primary_id += f"-{comment.id}"
            comments.append(comment)
        # Now let's test whether the previous comment is the parent of the next comment
        for index in range(len(comments)):
            children = find_children_recursively([comments[index]], ctx.request.url_root)
            assert children
            assert len(children) == 1
            assert isinstance(children, list)
            assert isinstance(children[0], dict)
            assert "children" in children[0]
            # Test for all comments except the last one
            if index != len(comments) - 1:
                # Find the children of the previous comment
                assert children[0]["children"]
                assert len(children[0]["children"]) == 1
                assert isinstance(children[0]["children"], list)
                assert isinstance(children[0]["children"][0], dict)
                # Assert that the next comment is in the children of the previous comment.
                assert children[0]["children"][0]["id"] == comments[index + 1].id
            # Test the last one
            else:
                assert children[0]["children"] == []


def test_response_children(app, client, test_user, test_data):
    with app.test_request_context() as ctx:
        # Test with invalid arguments
        assert response_children("", "") is None
        # Set the transaction user_id.
        with client.session_transaction() as session_transaction:
            session_transaction['user_id'] = test_user.id
        # Login as test_user.
        login_user(test_user)
        # Create an article with post request
        # We have already created an article and 10 comments
        article = Article.query.filter_by(title="Other Title").first()
        assert article
        comment = Comment.query.filter_by(content=f"Other Content-0").first()
        assert comment
        # Now let's use them as the arguments of response_children function
        assert response_children(article, ctx.request.url_root)


def test_add_comment(app, client, test_user):
    with app.test_request_context(
        method="POST",
        data={
            "primary_id": "Other Title-secondary",
            "add": True, "content":
            "Content from test_add_comment"
        }
    ) as ctx:
        # Test with invalid arguments
        assert add_comment(ctx.request, app.db, "") is None
        assert hasattr(ctx.request, "form")
        assert "primary_id" in ctx.request.form
        # Now test with valid arguments.
        # We had created an example article which title is 'Other Title'.
        article = Article.query.filter_by(title="Other Title").first()
        assert article
        # Set the transaction user_id.
        with client.session_transaction() as session_transaction:
            session_transaction['user_id'] = test_user.id
        # Login as test_user.
        login_user(test_user)
        # Test add_comment
        assert add_comment(ctx.request, app.db, article)


def test_update_comment(app, client, test_user):
    comment_id = Comment.query.filter_by(content="Content from test_add_comment").first().id
    with app.test_request_context(
        method="POST",
        data={
            "primary_id": f"Other Title-secondary-{comment_id}",
            "update": True,
            "content": "Update from test_add_comment"
        }
    ) as ctx:
        # Test with invalid arguments
        assert update_comment(ctx.request, app.db) is None
        assert hasattr(ctx.request, "form")
        assert "primary_id" in ctx.request.form
        # Now test with valid arguments.
        # Set the transaction user_id.
        with client.session_transaction() as session_transaction:
            session_transaction['user_id'] = test_user.id
        # Login as test_user.
        login_user(test_user)
        assert update_comment(ctx.request, app.db)
        assert hasattr(ctx.request, "form")
        assert "primary_id" in ctx.request.form


def test_like_dislike_comment(app, client, test_user):
    comment_id = Comment.query.filter_by(content="Update from test_add_comment").first().id
    with app.test_request_context(
        method="POST",
        data={
            "primary_id": f"Other Title-secondary-{comment_id}",
            "value": 1,
            "like_dislike": True
        }
    ) as ctx:
        # Test with invalid arguments
        assert like_dislike_comment(ctx.request, app.db, "") is None
        assert hasattr(ctx.request, "form")
        assert "primary_id" in ctx.request.form
        # Now test with valid arguments.
        # We had created an example article which title is 'Other Title'.
        article = Article.query.filter_by(title="Other Title").first()
        assert article
        # Set the transaction user_id.
        with client.session_transaction() as session_transaction:
            session_transaction['user_id'] = test_user.id
        # Login as test_user.
        login_user(test_user)
        # Test with invalid arguments
        assert like_dislike_comment(ctx.request, app.db, article)
        assert hasattr(ctx.request, "form")
        assert "primary_id" in ctx.request.form


def test_delete_comment(app, client, test_user):
    comment_id = Comment.query.filter_by(content="Update from test_add_comment").first().id
    with app.test_request_context(
        method="POST",
        data={
            "primary_id": f"Other Title-secondary-{comment_id}",
            "delete": True
        }
    ) as ctx:
        # Test with invalid arguments
        assert delete_comment(ctx.request, app.db, "") is None
        assert hasattr(ctx.request, "form")
        assert "primary_id" in ctx.request.form
        # Now test with valid arguments.
        # We had created an example article which title is 'Other Title'.
        article = Article.query.filter_by(title="Other Title").first()
        assert article
        # Set the transaction user_id.
        with client.session_transaction() as session_transaction:
            session_transaction['user_id'] = test_user.id
        # Login as test_user.
        login_user(test_user)
        # Test with invalid arguments
        assert delete_comment(ctx.request, app.db, article)
        assert hasattr(ctx.request, "form")
        assert "primary_id" in ctx.request.form


def test_query():
    # Test with invalid arguments
    assert query("", 1) is None
    # Test with valid arguments.
    d = {
        "indicativo": {
            "presente": {
                "io": "",
                "tu": "",
            },
            "imperfetto": {
                "io": "",
                "tu": ""
            }
        },
        "congiuntivo": {
            "presente": {
                "io": "",
                "tu": "",
            },
            "imperfetto": {
                "io": "",
                "tu": ""
            }
        }
    }
    test = {
        "indicativo": {
            "presente": {
                "io": "",
                "tu": ""
            },
            "imperfetto": {
                "tu": ""
            }
        },
        "congiuntivo": {
            "presente": {
                "io": "",
                "tu": ""
            },
            "imperfetto": {
                "tu": ""
            }
        }
    }
    keys = ["presente", "tu"]
    assert query(d, keys) == test


def test_get_article_info(app, client, test_user):
    with app.test_request_context():
        # We had created an example article which title is 'Other Title'.
        article = Article.query.filter_by(title="Other Title").first()
        assert article
        # Test with invalid arguments.
        assert get_article_info("") is None
        # Test with valid arguments.
        assert get_article_info(article)
        # Delete the article
        # Set the transaction user_id.
        with client.session_transaction() as session_transaction:
            session_transaction['user_id'] = test_user.id
        # Login as test_user.
        login_user(test_user)
        response = client.get("/article/Other Title/delete")
        assert response.status_code == 302
        assert "Redirecting" in response.data.decode()
        assert Article.query.filter_by(title="Other Title").first() is None


def test_get_all_articles(app):
    with app.test_request_context():
        all_articles = get_all_articles()
        assert isinstance(all_articles, list)
        assert len(all_articles) == 0


def test_get_user_articles(app, test_user):
    with app.test_request_context():
        # Test with invalid arguments
        assert get_user_articles("") is None
        # Test with a valid argument
        user_articles = get_user_articles(test_user)
        assert isinstance(user_articles, list)
        assert len(user_articles) == 0


def test_select_image(app):
    with app.test_request_context():
        # Test with invalid arguments
        assert select_image(1) is None
        # Test with different arguments
        assert select_image("username") == "letter-u.svg"
        assert select_image("new") == "letter-n.svg"
        assert select_image("dildeolupbiten") == "logo.svg"


def test_permitted(app):
    with app.test_request_context():
        # Test with invalid argument
        assert permitted("") is None
        # Test with valid argument
        assert permitted(app)
        assert permitted(app) == ["dildeolupbiten", "test_user"]


def test_html_code_format(app):
    # Test with invalid argument.
    assert HTMLCodeFormat(1) is None
    # Continue testing
    code = HTMLCodeFormat("hello")
    assert code
    highlighted = code.highlight()
    assert highlighted
    assert isinstance(highlighted, str)
    assert "</div>" not in highlighted
    # Test with valid arguments
    code = HTMLCodeFormat('[code="python"]\nprint("hello")\n[/code]')
    assert code
    highlighted = code.highlight()
    assert highlighted
    assert isinstance(highlighted, str)


def test_get_articles(app):
    # Test with invalid argument:
    assert not get_articles("")
    assert not get_articles([])
    assert not get_articles([{}])
    assert not get_articles([{"category": ""}])
    arg = [
        {"category": 'Programming / Web / Jinja'},
        {"category": 'Programming / Web / HTML'},
        {"category": 'Programming / GUI / Tkinter'},
        {"category": 'Programming / GUI / PyQT4'}
    ]
    result = get_articles(arg)
    assert result
    assert isinstance(result, dict)


def test_order_articles(app):
    # Test with invalid argument:
    assert not order_articles("")
    assert not order_articles([])
    arg = {
        "Programming": {
            "Web": {
                "Jinja",
                "HTML"
            },
            "GUI": {
                "Tkinter",
                "PyQT4"
            }
        }
    }
    result = order_articles(arg)
    assert result
    assert isinstance(result, list)
    assert all(isinstance(i, dict) and "category" in i for i in result)


def test_create_dict(app):
    # Test with invalid arguments
    assert create_dict(1, 2) is None
    assert create_dict("a", "b") is None
    assert create_dict(["a"], "b") is None
    # Test with valid argument
    res = create_dict(["a"], ["b"])
    assert res
    assert isinstance(res, dict)
    assert "a" in res
    assert res["a"]
    assert isinstance(res["a"], dict)
    assert "b" in res["a"]
    assert isinstance(res["a"]["b"], str)


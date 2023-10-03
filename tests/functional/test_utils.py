# -*- coding: utf-8 -*-

from dildeolupbiten.utils import *
from flask_login import login_user


def test_api_info():
    # Test with an invalid filename.
    assert api_info(1, "<url>") is None
    # Test with the valid filename.
    result = api_info(
        "./dildeolupbiten/api/italian_verbs/italian_verbs.md",
        "<url>"
    )
    assert result
    assert "<url>" in result


def test_render():
    # Render a not str value
    assert render(1) is None
    # Render a str value
    assert render("a")


def test_pygmentize():
    # Render a not str value
    assert pygmentize(1) is None
    # Render a str value
    assert pygmentize("a")


def test_count_attr(app, client, test_user, test_data):
    with app.test_request_context():
        # Test with invalid arguments
        assert count_attr("a", "b") is None
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


def test_orphan_comments():
    pass


def test_search_article():
    pass


def test_find_children_recursively():
    pass


def test_response_children():
    pass


def test_add_comment():
    pass


def test_update_comment():
    pass


def test_like_dislike_comment():
    pass


def test_delete_comment():
    pass


def test_query():
    pass


def test_update():
    pass


def test_get_article_info():
    pass


def test_get_all_articles():
    pass


def test_get_user_articles():
    pass


def test_select_image():
    pass


def test_permitted():
    pass

# -*- coding: utf-8 -*-

from flask_login import login_user

from dildeolupbiten.articles.models import Article
from dildeolupbiten.comments.models import Comment
from dildeolupbiten.likes_dislikes.models import LikeDislikeArticle, LikeDislikeComment


def test_create_article_get(client):
    response = client.get("/article/create")
    assert response.status_code == 302
    assert "Redirecting" in response.data.decode()


def test_create_article_post(app, client, test_user):
    with app.test_request_context():
        data = {
            "title": "Test",
            "description": "Description",
            "content": "Content",
            "image": "https://www.abbanews.eu/wp-content/uploads/2021/11/Fibonacci.jpg"
        }
        # Send a post request with an unauthorized user.
        response = client.post("/article/create", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
        assert response.status_code == 302
        assert "Redirecting" in response.data.decode()
        assert Article.query.filter_by(title="Test").first() is None
        # Now let's change the user. Set the transaction user_id.
        with client.session_transaction() as session_transaction:
            session_transaction['user_id'] = test_user.id
        # Login as test_user.
        login_user(test_user)
        # Send a post request with test user.
        response = client.post("/article/create", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
        assert response.status_code == 302
        assert "Redirecting" in response.data.decode()
        assert Article.query.filter_by(title="Test").first()


def test_view_article(client):
    response = client.get("/article/Test")
    assert response.status_code == 200


def test_create_comment(app, client, test_user):
    with app.test_request_context():
        data = {
            "content": "Test Content",
            "primary_id": "Test-secondary",
            "add": True
        }
        # Send a post request with an unauthorized user.
        response = client.post("/article/Test", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
        assert response.status_code == 404
        assert Comment.query.filter_by(content="Test Content").first() is None
        # Now let's change the user. Set the transaction user_id.
        with client.session_transaction() as session_transaction:
            session_transaction['user_id'] = test_user.id
        # Login as test_user.
        login_user(test_user)
        # Send a post request with test user.
        response = client.post("/article/Test", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
        assert response.status_code == 200
        assert Comment.query.filter_by(content="Test Content").first()


def test_update_comment(app, client, test_user):
    with app.test_request_context():
        # Get the comment owned by the test user.
        comment = Comment.query.filter_by(user_id=test_user.id).first()
        # Assert that the comment exists.
        assert comment
        data = {
            "content": "Update Content",
            "primary_id": f"Test-secondary-{comment.id}",
            "update": True
        }
        # Send a post request with an unauthorized user.
        response = client.post("/article/Test", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
        # Assert that the response status is Not Found.
        assert response.status_code == 404
        # Assert that the comment is not updated.
        assert Comment.query.filter_by(content="Update Content").first() is None
        # Now let's change the user. Set the transaction user_id.
        with client.session_transaction() as session_transaction:
            session_transaction['user_id'] = test_user.id
        # Login as test_user.
        login_user(test_user)
        # Send a post request with test user.
        response = client.post("/article/Test", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
        assert response.status_code == 200
        assert Comment.query.filter_by(content="Update Content").first()


def test_like_dislike(app, client, test_user):
    with app.test_request_context():
        # Get the article
        article = Article.query.filter_by(title="Test").first()
        # Assert that the article exists.
        assert article
        # Assert that the article has no like:
        assert LikeDislikeArticle.query.filter_by(article_id=article.id).first() is None
        # Get the comment owned by test user.
        comment = Comment.query.filter_by(user_id=test_user.id).first()
        # Assert that the comment exists.
        assert comment
        # Assert that the comment has no like.
        assert LikeDislikeComment.query.filter_by(comment_id=comment.id).first() is None
        data = {
            "primary_id": f"Test-secondary",
            "like_dislike": True,
            "value": 1  # means like
        }
        # Send a post request with an unauthorized user.
        response = client.post("/article/Test", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
        assert response.status_code == 404
        # Let's try to like the comment with the same unauthorized user.
        # Change the primary_id.
        data["primary_id"] = f"Test-secondary-{comment.id}"
        # Send a post request with an unauthorized user.
        response = client.post("/article/Test", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
        assert response.status_code == 404
        # Now let's change the user. Set the transaction user_id.
        with client.session_transaction() as session_transaction:
            session_transaction['user_id'] = test_user.id
        # Login as test_user.
        login_user(test_user)
        # Change the primary_id to article id.
        data["primary_id"] = "Test-secondary"
        # Send a post request with test user
        response = client.post("/article/Test", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
        assert response.status_code == 200
        assert LikeDislikeArticle.query.filter_by(article_id=article.id).first_or_404()
        # Change the primary_id to comment id.
        data["primary_id"] = f"Test-secondary-{comment.id}"
        # Send a post request with test user
        response = client.post("/article/Test", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
        assert response.status_code == 200
        assert LikeDislikeComment.query.filter_by(comment_id=comment.id).first()


def test_delete_comment(app, client, test_user):
    with app.test_request_context():
        comment = Comment.query.filter_by(user_id=test_user.id).first()
        # Assert that the comment exists.
        assert comment
        # Unauthorized user tries to delete a comment.
        data = {
            "primary_id": f"Test-secondary-{comment.id}",
            "delete": True
        }
        # Send a post request with an unauthorized user.
        response = client.post("/article/Test", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
        # Assert that the response status is Not Found.
        assert response.status_code == 404
        # Set the transaction user_id.
        with client.session_transaction() as session_transaction:
            session_transaction['user_id'] = test_user.id
        # Login as test_user.
        login_user(test_user)
        # Send the same post request with test user.
        response = client.post("/article/Test", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
        # Assert that the response status is success.
        assert response.status_code == 200
        # Check if the comment is deleted.
        assert Comment.query.filter_by(content="Update Content").first() is None


def test_update_article(app, client, test_user):
    with app.test_request_context():
        data = {
            "title": "Update Test",
            "description": "Update Description",
            "content": "Update Content",
            "image": "https://www.abbanews.eu/wp-content/uploads/2021/11/Fibonacci.jpg"
        }
        # Send a post request with an unauthorized user.
        response = client.post("/article/Test/update", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
        assert response.status_code == 302
        assert "Redirecting" in response.data.decode()
        assert Article.query.filter_by(title="Update Test").first() is None
        # Set the transaction user_id.
        with client.session_transaction() as session_transaction:
            session_transaction['user_id'] = test_user.id
        # Login as test_user.
        login_user(test_user)
        # Send the same post request with test user.
        response = client.post("/article/Test/update", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
        assert response.status_code == 302
        assert "Redirecting" in response.data.decode()
        assert Article.query.filter_by(title="Update Test").first()


def test_delete_article(app, client, test_user):
    with app.test_request_context():
        # Get a response with an unauthorized user.
        response = client.get("/article/Update Test/delete")
        assert response.status_code == 302
        assert "Redirecting" in response.data.decode()
        assert Article.query.filter_by(title="Update Test").first()
        # Set the transaction user_id.
        with client.session_transaction() as session_transaction:
            session_transaction['user_id'] = test_user.id
        # Login as test_user.
        login_user(test_user)
        # Get a response with test user.
        response = client.get("/article/Update Test/delete")
        assert response.status_code == 302
        assert "Redirecting" in response.data.decode()
        assert Article.query.filter_by(title="Update Test").first() is None

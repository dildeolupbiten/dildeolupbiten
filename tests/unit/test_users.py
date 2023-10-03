# -*- coding: utf-8 -*-

import os
from dildeolupbiten.users.models import User
from flask_login import login_user, logout_user, current_user


def test_register(app, client, test_user):
    with app.test_request_context():
        # Use a register that already exists.
        data = {
            "email": test_user.email,
            "password": "dildeolupbiten1234",
            "confirm_password": "dildeolupbiten1234",
            "username": "dildeolupbiten",
            "image": os.path.join(app.root_path, "static/images/logo.svg")
        }
        # Submit and validate.
        # Send a post request with a register that already exists.
        response = client.post(
            "/register",
            data=data,
            headers={"X-Requested-With": "XMLHttpRequest"}
        )
        assert b"Register" in response.data
        assert response.status_code == 200
        # Use the password of the test user.
        # Change the email.
        data["email"] = "dildeolupbiten@gmail.com"
        # Send a post request with this email.
        response = client.post(
            "/register",
            data=data,
            headers={"X-Requested-With": "XMLHttpRequest"}
        )
        assert response.status_code == 302
        assert b"Redirecting" in response.data


def test_login(client, test_user):
    data = {
        "email": test_user.email,
        "password": "wrong password"
    }
    # Send a post request with wrong credentials.
    response = client.post(
        "/login",
        data=data,
        headers={"X-Requested-With": "XMLHttpRequest"}
    )
    assert response.status_code == 404
    assert b"Redirecting" in response.data
    # Use the password of the test user.
    data["password"] = "test1234"
    # Send a post request with test user credentials.
    response = client.post(
        "/login",
        data=data,
        headers={"X-Requested-With": "XMLHttpRequest"})
    assert response.status_code == 302
    assert b"Redirecting" in response.data
    # Try to log in as the user that is recently registered.
    data = {"email": "dildeolupbiten@gmail.com", "password": "dildeolupbiten1234"}
    # Send a post request with the new credentials.
    response = client.post(
        "/login",
        data=data,
        headers={"X-Requested-With": "XMLHttpRequest"}
    )
    assert response.status_code == 302
    assert b"Redirecting" in response.data


def test_view_user_articles(client):
    for i in ["", "/all_articles"]:
        # Send a post request for a view that doesn't exist.
        response = client.get("/user/invalid_username" + i)
        assert response.status_code == 404
        # Send a post request for a view that exists.
        response = client.get("/user/test_user" + i)
        assert response.status_code == 200
        # Send a post request for a view that exists.
        response = client.get("/user/dildeolupbiten" + i)
        assert response.status_code == 200


def test_update_user(app, client):
    with app.test_request_context():
        response = client.get("/account")
        assert response.status_code == 302
        assert b"Redirecting" in response.data
        data = {
            "username": "dildeolupbiten",
            "email": "test@test.com"
        }
        # Send a post request without credentials
        response = client.post(
            "/account",
            data=data,
            headers={"X-Requested-With": "XMLHttpRequest"}
        )
        assert response.status_code == 302
        assert b"Redirecting" in response.data
        user = User.query.filter_by(username="dildeolupbiten").first()
        # Assert that the email hasn't changed.
        assert user.email != "test@test.com"
        # Now let's change the user. Set the transaction user_id.
        with client.session_transaction() as session_transaction:
            session_transaction['user_id'] = user.id
        # Login as test_user.
        login_user(user)
        # Send a post request without credentials
        response = client.post(
            "/account",
            data=data,
            headers={"X-Requested-With": "XMLHttpRequest"}
        )
        assert response.status_code == 302
        assert b"Redirecting" in response.data
        # Assert that the email has changed.
        assert User.query.filter_by(username="dildeolupbiten").first().email == "test@test.com"
        # Change the email back to original
        data["email"] = "dildeolupbiten@gmail.com"
        # Send a post request without credentials
        response = client.post(
            "/account",
            data=data,
            headers={"X-Requested-With": "XMLHttpRequest"}
        )
        assert response.status_code == 302
        assert b"Redirecting" in response.data
        # Assert that the email has changed to original.
        assert User.query.filter_by(username="dildeolupbiten").first().email == "dildeolupbiten@gmail.com"


def test_reset_request(client):
    # Send a get request.
    response = client.get("/reset_password")
    assert response.status_code == 200
    data = {"email": "dildeolupbiten@gmail.com"}
    # Send a post request, this request sends an email.
    response = client.post(
        "/reset_password",
        data=data,
        headers={"X-Requested-With": "XMLHttpRequest"}
    )
    assert response.status_code == 302
    assert b"Redirecting" in response.data


def test_reset_password(app, client):
    with app.test_request_context():
        # Send a get request.
        response = client.get("/reset_password")
        assert response.status_code == 200
        # Get the user
        user = User.query.filter_by(username="dildeolupbiten").first()
        # We will use get_reset_token() function to create a new token.
        token = user.get_reset_token()
        # Verify the token
        user = User.verify_reset_token(token)
        assert user
        data = {"password": "new1234", "confirm_password": "new1234"}
        response = client.post(
            f"/reset_password/{token}",
            data=data,
            headers={"X-Requested-With": "XMLHttpRequest"}
        )
        assert response.status_code == 302
        assert b"Redirecting" in response.data
        # Let's try to log in with the old password.
        data = {
            "email": "dildeolupbiten@gmail.com",
            "password": "dildeolupbiten1234"
        }
        # Send a post request with the old password.
        response = client.post(
            "/login",
            data=data,
            headers={"X-Requested-With": "XMLHttpRequest"}
        )
        assert response.status_code == 404
        assert b"Redirecting" in response.data
        # Change the password.
        data["password"] = "new1234"
        # Send a post request with the new password.
        response = client.post(
            "/login",
            data=data,
            headers={"X-Requested-With": "XMLHttpRequest"}
        )
        assert response.status_code == 302
        assert b"Redirecting" in response.data


def test_delete_user(app, client):
    with app.test_request_context():
        # Send a get request.
        response = client.get("/user/dildeolupbiten/delete")
        assert response.status_code == 302
        # Let's check whether the user exists.
        user = User.query.filter_by(username="dildeolupbiten").first()
        # Assert that user exists.
        assert user
        # Now let's change the user. Set the transaction user_id.
        with client.session_transaction() as session_transaction:
            session_transaction['user_id'] = user.id
        # Login as test_user.
        login_user(user)
        response = client.get("/user/dildeolupbiten/delete")
        assert response.status_code == 302
        # Assert user is deleted.
        assert User.query.filter_by(username="dildeolupbiten").first() is None


def test_logout(client, test_user):
    # Send a get request.
    response = client.get("/logout")
    assert response.status_code == 302
    assert b"Redirecting" in response.data
    assert hasattr(current_user, "username") is False
    with client.session_transaction() as session_transaction:
        session_transaction['user_id'] = test_user.id
    # Login as test_user.
    login_user(test_user)
    assert hasattr(current_user, "username")
    # Now log out as.
    logout_user()
    # Let's assert that test_user successfuly logged out.
    assert hasattr(current_user, "username") is False

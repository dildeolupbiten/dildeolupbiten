# -*- coding: utf-8 -*-

import os
from dildeolupbiten.users.models import User
from flask_login import login_user


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
        response = client.post("/register", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
        assert b"Register" in response.data
        assert response.status_code == 200
        # Use the password of the test user.
        # Change the email.
        data["email"] = "dildeolupbiten@gmail.com"
        # Send a post request with this email.
        response = client.post("/register", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
        assert response.status_code == 302
        assert b"Redirecting" in response.data


def test_login(client, test_user):
    data = {
        "email": test_user.email,
        "password": "wrong password"
    }
    # Send a post request with wrong credentials.
    response = client.post("/login", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
    assert response.status_code == 404
    assert "Redirecting" in response.data.decode()
    # Use the password of the test user.
    data["password"] = "test1234"
    # Send a post request with test user credentials.
    response = client.post("/login", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
    assert response.status_code == 302
    assert b"Redirecting" in response.data
    # Try to log in as the user that is recently registered.
    data = {"email": "dildeolupbiten@gmail.com", "password": "dildeolupbiten1234"}
    # Send a post request with the new credentials.
    response = client.post("/login", data=data, headers={"X-Requested-With": "XMLHttpRequest"})
    assert response.status_code == 302
    assert b"Redirecting" in response.data


def test_views(client):
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


def test_delete(app, client):
    with app.test_request_context():
        # Send a post request without login.
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

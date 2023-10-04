# -*- coding: utf-8 -*-

import os
import pytest

from dildeolupbiten import db, create_app, bcrypt
from dildeolupbiten.users.models import User


@pytest.fixture
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    app.config['WTF_CSRF_ENABLED'] = False
    app.db = db
    yield app


@pytest.fixture
def client(app):
    yield app.test_client()


@pytest.fixture
def runner(app):
    yield app.test_cli_runner()


@pytest.fixture
def test_user(app):
    with app.test_request_context():
        test_user = User.query.filter_by(username="test_user").first()
        if not test_user:
            test_user = User(
                username="test_user",
                password=bcrypt.generate_password_hash("test1234").decode("utf-8"),
                email=os.environ["MAIL_USERNAME"],
                image=os.path.join(app.root_path, "static/images/logo.svg"),
                permission=True
            )
            db.session.add(test_user)
            db.session.commit()
        yield test_user


@pytest.fixture
def test_data(app):
    yield lambda s: {
        "title": f"{s} Title",
        "description": f"{s} Description",
        "content": f"{s} Content",
        "image": "https://www.abbanews.eu/wp-content/uploads/2021/11/Fibonacci.jpg"
    }

# -*- coding: utf-8 -*-


def test_categories(client):
    # Send a get request
    response = client.get("/articles")
    assert response.status_code == 200
    response = client.post(
        "/articles",
        data={"articles": True},
        headers={"X-Requested-With": "XMLHttpRequest"}
    )
    assert response.status_code == 200

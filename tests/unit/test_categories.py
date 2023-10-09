# -*- coding: utf-8 -*-


def test_categories(client):
    # Send a get request
    response = client.get("/categories")
    assert response.status_code == 200
    response = client.post(
        "/categories",
        data={"categories": True},
        headers={"X-Requested-With": "XMLHttpRequest"}
    )
    assert response.status_code == 200

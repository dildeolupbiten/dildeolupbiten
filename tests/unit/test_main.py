# -*- coding: utf-8 -*-

def test_get_requests(client):
    for view in ["/", "/about", "/all_articles"]:
        response = client.get(view)
        assert response.status_code == 200


def test_post_requests(client):
    for view, key in [["/", "articles"], ["/all_articles", "all_articles"]]:
        response = client.post(
            view,
            data={key: True},
            headers={"X-Requested-With": "XMLHttpRequest"}
        )
        assert response.status_code == 200


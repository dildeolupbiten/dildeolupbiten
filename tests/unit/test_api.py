# -*- coding: utf-8 -*-

import json


def test_get_requests(client):
    # Send a get request
    response = client.get("/api/italian_verbs")
    assert response.status_code == 200
    # Send a get request with an empty data
    response = client.get("/api/italian_verbs?data={\"verb\": \"\"}")
    assert response.status_code == 200
    # Test if the response data is an empty dict
    assert json.loads(response.data) == {}
    # Send a get request with a valid data
    response = client.get("/api/italian_verbs?data={\"verb\": \"essere\"}")
    assert response.status_code == 200
    data = json.loads(response.data)
    # Assert that data has value
    assert data
    # Assert that type of the data is list
    assert isinstance(data, list)
    # Assert that length of the list is 1
    assert len(data) == 1
    # Assert that the item of the list is a dict
    assert isinstance(data[0], dict)
    assert "verb" in data[0]
    assert data[0]["verb"] == "essere"
    assert "conjugations" in data[0]
    # The below data is also valid.
    response = client.get("/api/italian_verbs?data={\"verb\": [\"essere\", \"avere\"]}")
    assert response.status_code == 200
    data = json.loads(response.data)
    # Assert that length of the data is 2
    assert len(data) == 2
    assert data[0]["verb"] == "essere"
    assert data[1]["verb"] == "avere"
    # The below data is also valid:
    response = client.get(
        "/api/italian_verbs?data={\"verb\": [\"essere\", \"avere\"], \"modality\": \"indicativo\"}"
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]["verb"] == "essere"
    assert data[1]["verb"] == "avere"
    assert list(data[0]["conjugations"]) == ["indicativo"]
    assert list(data[1]["conjugations"]) == ["indicativo"]

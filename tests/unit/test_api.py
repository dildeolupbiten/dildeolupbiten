# -*- coding: utf-8 -*-

import json


def test_get_requests(client):
    for view in ["/api/italian_verbs", "/api/italian_verbs?data={\"verb\": \"\"}"]:
        response = client.get(view)
        assert response.status_code == 200
        if "data" in view:
            assert json.loads(response.data) == []

def test_query_requires_api_key(client):
    response = client.post("/query", json={"q": "test"})
    assert response.status_code == 401

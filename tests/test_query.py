def test_query_endpoint(client):
    payload = {
        "q": "¿Qué es LlamaIndex?",
        "top_k": 3,
        "stream": False,
    }

    response = client.post(
        "/query",
        json=payload,
        headers={"X-API-Key": "super-secret-key-change-me"},
    )

    assert response.status_code == 200

    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert "retrieval_params" in data

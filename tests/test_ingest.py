def test_ingest_endpoint(client):
    files = {
        "files": (
            "test.txt",
            b"LlamaIndex es un framework para RAG.",
            "text/plain",
        )
    }

    response = client.post(
        "/ingest",
        files=files,
        headers={"X-API-Key": "super-secret-key-change-me"},
    )

    assert response.status_code == 200

    data = response.json()
    assert "ingested" in data
    assert "skipped" in data
    assert "errors" in data

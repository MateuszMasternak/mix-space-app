def assert_status_codes(client,
                        url,
                        get=405,
                        post=501,
                        put=501,
                        patch=501,
                        delete=501,
                        _all=-1):
    if _all != -1:
        get = post = put = patch = delete = _all

    response = client.get(url)
    assert response.status_code == get

    response = client.post(url)
    assert response.status_code == post

    response = client.put(url)
    assert response.status_code == put

    response = client.patch(url)
    assert response.status_code == patch

    response = client.delete(url)
    assert response.status_code == delete
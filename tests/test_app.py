def test_app_is_testing(app):
    assert app.config['TESTING']


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Last updated:" in response.data


def test_data_page(client):
    response = client.get('/data')
    assert response.status_code == 200
    assert b"temperature" in response.data


def test_wrong_url(client):
    response = client.get('/wrong/url')
    assert response.status_code == 404

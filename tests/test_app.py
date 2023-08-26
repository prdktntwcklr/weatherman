from weatherman import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_hello(client):
    response = client.get('/')

    assert response.status == '200 OK'
    assert b'Hello World!' in response.data

from weatherman import app

def test_hello():
    response  = app.test_client().get('/')

    assert response.status == '200 OK'
    assert response.data == b'Hello World!'

from weatherman import app

def test_hello():
    response  = app.test_client().get('/')

    assert response.status == '200 OK'
    assert b'Hello World!' in response.data

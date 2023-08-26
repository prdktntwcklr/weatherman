from weatherman import create_app

# TODO: tests should be rewritten to account for factory method

def test_hello():
    app = create_app()

    response = app.test_client().get('/')

    assert response.status == '200 OK'
    assert b'Hello World!' in response.data

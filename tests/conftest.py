import pytest

from weatherman import create_app


@pytest.fixture()
def app():
    # create new app in testing mode
    app = create_app('testing')

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def jinja(app):
    return app.jinja_env

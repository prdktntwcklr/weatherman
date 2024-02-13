import os

from datetime import datetime
from flask import Flask, render_template

def create_app(test_config=None):
    # default env file
    env_file = '.env.example'

    # check if user provided env file exists and update if necessary
    if os.path.isfile('.env'):
        env_file = '.env'

    with open(env_file, 'r') as fh:
        configs = dict(
            tuple(line.replace('\n', '').replace('\"', '').split('='))
            for line in fh.readlines() if not line.startswith('#')
        )

    os.environ.update(configs)

    # base directory is one level up from this file
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_FILE = os.environ.get("DATABASE_FILE")

    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=os.path.join(BASE_DIR, DATABASE_FILE),
    )

    print(f"Database file used is: {app.config.get('DATABASE')}")

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from . import db
    db.init_app(app)

    with app.app_context():
        db.init_db()

    @app.route('/')
    def index():
        rows = db.get_rows()

        return render_template("index.html", data=rows)

    @app.route("/data")
    def data():
        rows = db.get_rows()

        return render_template("data.html", data=rows)

    @app.template_filter('strftime')
    def pretty_date(dateString, fmt='%Y-%m-%dT%H:%M+00:00'):
        dt = datetime.strptime(dateString, fmt)
        return dt.strftime('%Y-%m-%d %H:%M')

    return app

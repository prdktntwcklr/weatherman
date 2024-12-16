"""main Flask application"""

from config import config
from datetime import datetime
from flask import Flask, render_template
from . import db


# create_app factory is autodetected by Flask
def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    print(f"Database file used is: {app.config.get('DATABASE')}")

    db.init_app(app)

    with app.app_context():
        db.init_db()

    @app.route("/")
    def index():
        rows = db.get_rows()

        return render_template("index.html", data=rows)

    @app.route("/data")
    def data():
        rows = db.get_rows()

        return render_template("data.html", data=rows)

    @app.template_filter("strftime")
    def pretty_date(date_string, fmt="%Y-%m-%dT%H:%M+00:00"):
        dt = datetime.strptime(date_string, fmt)
        return dt.strftime("%Y-%m-%d %H:%M")

    return app

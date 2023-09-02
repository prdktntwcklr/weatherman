from flask import Flask, render_template, g
import os
from datetime import datetime

def create_app(test_config = None):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE_FILE =  "../tools/examples/weather.db"

    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=os.path.join(BASE_DIR, DATABASE_FILE),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from . import db
    db.init_app(app)

    @app.route('/')
    def index():
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT time, temperature, humidity FROM weather ORDER BY ROWID DESC LIMIT 1")

        rows = cursor.fetchall()

        return render_template("index.html", data = rows)

    @app.route("/data")
    def data():
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT time, temperature, humidity FROM weather")
        
        rows = cursor.fetchall()

        return render_template("data.html", data = rows)
    
    @app.template_filter('strftime')
    def pretty_date(dateString, fmt='%Y-%m-%dT%H:%M+00:00'):
        dt = datetime.strptime(dateString, fmt)
        return dt.strftime('%Y-%m-%d %H:%M:00') 
    
    return app

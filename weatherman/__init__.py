from flask import Flask, render_template, g
import os
import sqlite3

def create_app(test_config = None):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=os.path.join(BASE_DIR, "../tools/examples/weather.db"),
    )

    from . import db
    db.init_app(app)

    @app.route('/')
    def hello():
        msg = "Hello World!"

        return render_template("hello.html", message = msg)

    @app.route("/data")
    def data():
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM weather")
        allData = cursor.fetchall()
        
        return render_template("data.html", data = allData)
    
    return app


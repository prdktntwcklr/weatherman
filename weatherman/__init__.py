from flask import Flask, render_template, g
import os
import sqlite3

# need to make sure we get the path correct from the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "../tools/examples/weather.db")

app = Flask(__name__)

@app.route('/')
def hello():
    msg = "Hello World!"

    return render_template("hello.html", message = msg)

@app.route("/data")
def data():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM weather")
    allData = cursor.fetchall()
    
    return render_template("data.html", data = allData)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run()

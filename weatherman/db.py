import os
import sqlite3

from flask import current_app, g


def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect(current_app.config['DATABASE'])

        # needed to access columns by name
        db.row_factory = sqlite3.Row

    return db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db_path = current_app.config['DATABASE']

    # check if database file does not exist yet
    if not os.path.exists(db_path):
        with current_app.open_resource("schema.sql") as f:
            db = sqlite3.connect(db_path)
            db.executescript(f.read().decode("utf8"))


def get_rows():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT time, temperature, humidity FROM database")

    return cursor.fetchall()


def init_app(app):
    app.teardown_appcontext(close_db)

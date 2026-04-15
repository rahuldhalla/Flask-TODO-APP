from flask import Flask
from tinydb import TinyDB

from routes import bp as todo_bp

DB_PATH = "db.json"


app = Flask(__name__)
app.extensions["tinydb"] = TinyDB(DB_PATH)
app.register_blueprint(todo_bp)


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query

app = Flask(__name__)
# creating tinydb
DB_PATH = 'db.json'
db = TinyDB(DB_PATH)


def get_next_todo_id():
    """Return a stable, unique id for a new todo item."""
    todo_list = db.all()
    if not todo_list:
        return 1
    return max(todo.get("id", 0) for todo in todo_list) + 1


@app.route("/")
def root():
    todo_list = db.all()
    return render_template('index.html', todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    # add new item
    title = (request.form.get("title") or "").strip()
    if not title:
        return redirect(url_for("root"))

    db.insert({'id': get_next_todo_id(), 'title': title, 'complete': False})
    return redirect(url_for("root"))


@app.route("/update", methods=["POST"])
def update():
    # update the todo title
    todo_db = Query()
    new_text = request.form.get('inputField')
    todo_id = request.form.get('hiddenField')
    db.update({"title": new_text}, todo_db.id == int(todo_id))
    return redirect(url_for("root"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # delete the todo
    todo_db = Query()
    db.remove(todo_db.id == todo_id)
    return redirect(url_for("root"))


@app.route("/complete/<int:todo_id>")
def complete(todo_id):
    # mark complete
    todo_db = Query()
    db.update({"complete": True}, todo_db.id == todo_id)
    return redirect(url_for("root"))


if __name__ == '__main__':
    app.run(debug=True)

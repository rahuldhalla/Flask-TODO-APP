from flask import Blueprint, current_app, redirect, render_template, request, url_for
from tinydb import Query

bp = Blueprint("todo", __name__)


def get_db():
    return current_app.extensions["tinydb"]


def get_next_todo_id():
    """Return a stable, unique id for a new todo item."""
    todo_list = get_db().all()
    if not todo_list:
        return 1
    return max(todo.get("id", 0) for todo in todo_list) + 1


@bp.route("/")
def root():
    todo_list = get_db().all()
    return render_template("index.html", todo_list=todo_list)


@bp.route("/add", methods=["POST"])
def add():
    title = (request.form.get("title") or "").strip()
    if not title:
        return redirect(url_for("todo.root"))

    get_db().insert({"id": get_next_todo_id(), "title": title, "complete": False})
    return redirect(url_for("todo.root"))


@bp.route("/update", methods=["POST"])
def update():
    todo_db = Query()
    new_text = request.form.get("inputField")
    todo_id = request.form.get("hiddenField")
    get_db().update({"title": new_text}, todo_db.id == int(todo_id))
    return redirect(url_for("todo.root"))


@bp.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo_db = Query()
    get_db().remove(todo_db.id == todo_id)
    return redirect(url_for("todo.root"))


@bp.route("/complete/<int:todo_id>")
def complete(todo_id):
    todo_db = Query()
    get_db().update({"complete": True}, todo_db.id == todo_id)
    return redirect(url_for("todo.root"))

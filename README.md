# Flask TODO App

A lightweight task manager built with **Flask** and **TinyDB**. This project demonstrates how to build a CRUD-style web application using server-rendered HTML templates, simple routes, and a file-based JSON database.

---

## Introduction

This application lets users:

- Create new tasks.
- View all saved tasks.
- Mark tasks as completed.
- Edit existing task text.
- Delete tasks.

The app is intentionally minimal and beginner-friendly: it has a single Flask application (`app.py`), one template (`templates/index.html`), and a TinyDB JSON file (`db.json`) for persistence.

---

## Project Structure

```text
Flask-TODO-APP/
├── app.py                  # Flask routes + TinyDB logic
├── db.json                 # Local TinyDB storage file
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Main UI (form, list, update popup)
└── screenshot/             # Optional screenshots used in docs
```

---

## How the Application Works

### 1) Backend (`app.py`)

The Flask app initializes TinyDB and exposes route handlers that process form submissions and user actions.

#### App and database initialization

- `app = Flask(__name__)` creates the Flask application instance.
- `DB_PATH = 'db.json'` defines where TinyDB stores records.
- `db = TinyDB(DB_PATH)` opens/creates the JSON database file.

#### ID generation

`get_next_todo_id()`:

- Reads all todo items with `db.all()`.
- Returns `1` when the database is empty.
- Otherwise returns `max(existing_ids) + 1`.

This gives each task a stable integer `id`.

#### Route-by-route behavior

- `GET /` → `root()`
  - Loads all todos from TinyDB.
  - Renders `templates/index.html` with `todo_list`.

- `POST /add` → `add()`
  - Reads `title` from form data.
  - Trims whitespace and prevents empty submissions.
  - Inserts a new todo object:
    - `id` (generated)
    - `title` (user text)
    - `complete` (`False` by default)
  - Redirects back to `/`.

- `POST /update` → `update()`
  - Reads `inputField` (new title) and `hiddenField` (todo id) from form.
  - Uses TinyDB `Query()` to locate matching record by `id`.
  - Updates the `title`.
  - Redirects to `/`.

- `GET /delete/<int:todo_id>` → `delete(todo_id)`
  - Removes the todo whose `id` matches `todo_id`.
  - Redirects to `/`.

- `GET /complete/<int:todo_id>` → `complete(todo_id)`
  - Updates the matching todo and sets `complete` to `True`.
  - Redirects to `/`.

---

### 2) Frontend template (`templates/index.html`)

The UI is rendered using Jinja templating and includes basic CSS + JavaScript.

#### Main UI pieces

- **Task input form** (`action="/add"`, `method="POST"`)
  - Sends new task text to the add route.

- **Task list rendering**
  - Iterates over `todo_list` from Flask.
  - Displays active and completed todos with different styles.
  - Shows action buttons for complete, edit, and delete.

- **Edit popup modal**
  - Hidden overlay shown by clicking the edit button.
  - Pre-fills current task text and id.
  - Submits to `/update` via POST.

#### JavaScript behavior

- Updates a live date/time display every second.
- `openPopup(id)`:
  - Reads current task text from the page.
  - Writes text/id into popup form fields.
  - Shows the popup container.
- `closePopup()` hides popup (defined but not bound to a dedicated close button in current template).

---

### 3) Data model (`db.json`)

Each todo item is stored as a JSON object similar to:

```json
{
  "id": 3,
  "title": "Buy groceries",
  "complete": false
}
```

Because TinyDB is file-based, data persists between server restarts as long as `db.json` remains in place.

---

## Prerequisites

- Python **3.8+** recommended.
- `pip` package manager.
- Internet access for initial dependency install.

---

## Setup Instructions

### 1) Clone the repository

```bash
git clone <your-repository-url>
cd Flask-TODO-APP
```

### 2) (Recommended) Create and activate a virtual environment

#### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

---

## How to Run the Web Application

From the project root:

```bash
python app.py
```

Flask starts in debug mode (as configured in `app.py`) and serves the app locally.

Open your browser at:

- `http://127.0.0.1:5000`

You should see the TODO interface where you can add, update, complete, and delete tasks.

---

## Typical User Flow

1. Enter text in **“Add Your Task Here”** and click `+`.
2. Task appears in the active list.
3. Click ✔ to mark it completed.
4. Click ✏ to open the edit popup, modify text, and save.
5. Click 🗑 to delete a task.

---

## Development Notes

- The app currently uses `GET` requests for delete/complete actions through anchor links.
- Completing a task is one-way in current logic (there is no “mark incomplete” route).
- Input validation is minimal (empty title prevented on add; update does not currently trim/validate).
- For production usage, consider:
  - Disabling `debug=True`.
  - Adding CSRF protection.
  - Switching to a production WSGI server (e.g., Gunicorn).
  - Adding form validation and error handling.

---

## Troubleshooting

- **`ModuleNotFoundError: No module named 'flask'`**
  - Activate your virtual environment and reinstall requirements.

- **Port 5000 already in use**
  - Stop the conflicting process, or run Flask on another port.

- **Changes not reflected in browser**
  - Hard refresh the page and ensure the server is still running.

---

## License

If you plan to distribute this project, add a `LICENSE` file (for example, MIT) and reference it here.

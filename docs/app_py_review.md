# app.py Code Review

## Summary
`app.py` is concise and functional for a small TODO app, but it would benefit from stronger input validation, safer HTTP method usage, clearer separation of concerns, and Flask configuration patterns that scale better.

## Findings

1. **Mutating routes use GET instead of POST/DELETE/PATCH**
   - `/delete/<int:todo_id>` and `/complete/<int:todo_id>` mutate server state but are currently GET routes.
   - Recommendation: switch to `POST` for form-driven actions (or `DELETE`/`PATCH` with JS clients) to avoid accidental crawlers/bookmarks causing writes and to align with HTTP semantics.

2. **Insufficient validation and error handling in `/update`**
   - `todo_id` is cast directly with `int(todo_id)` and `new_text` is used without normalization/empty check.
   - Recommendation: validate both fields (`strip`, non-empty title, numeric id), handle invalid values with `abort(400)` or flash a message.

3. **Database and query objects are repeated in handlers**
   - Each endpoint constructs `Query()` and directly accesses global `db`.
   - Recommendation: centralize DB access in helper/service functions to improve testability and readability.

4. **Application factory pattern is not used**
   - `app = Flask(__name__)` and `db = TinyDB(...)` are module-level globals.
   - Recommendation: migrate to `create_app()` and inject config/DB path. This is the Flask best-practice baseline for tests and multi-env deployment.

5. **`debug=True` is hardcoded in source**
   - `app.run(debug=True)` should not be committed for production flows.
   - Recommendation: rely on `FLASK_DEBUG` / environment configuration, or use config classes.

6. **ID generation is vulnerable to race conditions**
   - `get_next_todo_id()` reads all records and computes `max + 1`.
   - Recommendation: use UUIDs or an atomic counter table/metadata value if concurrent writes are possible.

7. **Naming clarity can improve**
   - Form keys like `inputField` and `hiddenField` are generic and reduce readability.
   - Recommendation: use explicit names such as `title` and `todo_id` in forms and handlers.

8. **No user-facing feedback on invalid operations**
   - Empty title in `/add` silently redirects.
   - Recommendation: use `flash()` messages and render validation feedback in templates.

## Suggested Refactor Plan (incremental)
1. Convert delete/complete to `POST` and update templates accordingly.
2. Add a shared `parse_todo_id()` and `normalize_title()` helper with 400 responses for invalid input.
3. Extract CRUD helpers into a separate module (`todo_service.py`).
4. Introduce `create_app(config=None)` and initialize TinyDB from config.
5. Move runtime config to environment-driven settings and remove hardcoded debug mode.

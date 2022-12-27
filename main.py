import uuid

from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

from database import (
    get_db,
    create_todo,
    delete_todo,
    get_todo,
    get_todos,
    update_todo,
    search_todos,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
db = get_db()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    session_key = request.cookies.get("session_key", uuid.uuid4().hex)
    todos = get_todos(db, session_key)
    context = {"request": request, "todos": todos, "title": "Home"}
    response = templates.TemplateResponse("home.html", context)
    response.set_cookie(key="session_key", value=session_key, expires=259200)  # 3 days
    return response


@app.post("/add", response_class=HTMLResponse)
def post_add(request: Request, content: str = Form(...)):
    session_key = request.cookies.get("session_key", "")
    todo = create_todo(db, content=content, session_key=session_key)
    context = {"request": request, "todo": todo}
    return templates.TemplateResponse("todo/item.html", context)


@app.get("/edit/{item_id}", response_class=HTMLResponse)
def get_edit(request: Request, item_id: int):
    todo = get_todo(db, item_id)
    context = {"request": request, "todo": todo}
    return templates.TemplateResponse("todo/form.html", context)


@app.put("/edit/{item_id}", response_class=HTMLResponse)
def put_edit(request: Request, item_id: int, content: str = Form(...)):
    todo = update_todo(db, item_id, content)
    context = {"request": request, "todo": todo}
    return templates.TemplateResponse("todo/item.html", context)


@app.delete("/delete/{item_id}", response_class=Response)
def delete(item_id: int):
    delete_todo(db, item_id)


@app.get("/search", response_class=HTMLResponse)
def get_search(request: Request, search: Optional[str] = None):
    session_key = request.cookies.get("session_key", "")
    todos = search_todos(db, session_key, search)
    if todos:
        context = {"request": request, "todos": todos}
        return templates.TemplateResponse("todo/items.html", context)
    else:
        context = {"request": request}
        return templates.TemplateResponse("todo/no_items.html", context)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

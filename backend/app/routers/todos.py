from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.connectors import todos

router = APIRouter(prefix="/todos")


class TodoBody(BaseModel):
    text: str
    remind_at: str | None = None       # ISO datetime; naive = server-local time
    notify_via: list[str] | None = None  # telegram / whatsapp / email


class TodoUpdate(BaseModel):
    text: str | None = None
    done: bool | None = None
    remind_at: str | None = None
    notify_via: list[str] | None = None
    clear_reminder: bool = False


@router.get("")
def list_todos():
    return {"items": todos.all_todos()}


@router.post("")
def add_todo(body: TodoBody):
    try:
        return todos.add(body.text, body.remind_at, body.notify_via)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{item_id}")
def update_todo(item_id: int, body: TodoUpdate):
    fields: dict = {}
    if body.text is not None:
        fields["text"] = body.text
    if body.done is not None:
        fields["done"] = body.done
    if body.clear_reminder:
        fields["remind_at"] = None
        fields["notify_via"] = []
    else:
        if body.remind_at is not None:
            fields["remind_at"] = body.remind_at
        if body.notify_via is not None:
            fields["notify_via"] = body.notify_via
    if not fields:
        raise HTTPException(status_code=400, detail="Nothing to update.")
    try:
        return todos.update(item_id, **fields)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{item_id}")
def delete_todo(item_id: int):
    try:
        return {"deleted": todos.delete_by_id(item_id)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

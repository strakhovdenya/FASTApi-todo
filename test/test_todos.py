from starlette import status
from ..routers.auth import get_current_user
from ..routers.todos import get_db, NOT_FOUND_DETAIL
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_todos):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {'priority': 2,
         'id': 1,
         'title': 'learn code',
         'owner_id': 1,
         'description': 'learn code every day',
         'complete': False}
    ]

def test_read_one_authenticated(test_todos):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
         'priority': 2,
         'id': 1,
         'title': 'learn code',
         'owner_id': 1,
         'description': 'learn code every day',
         'complete': False
    }

def test_read_one_authenticated_not_found(test_todos):
    response = client.get("/todos/todo/111")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': NOT_FOUND_DETAIL}

def test_create_todo_authenticated(test_todos):
    request_data = {
        'priority': 5,
        'title': 'new todo',
        'owner_id': 1,
        'description': 'new todo description',
        'complete': False
    }
    response = client.post("/todos/todo", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestSessionLocal()
    model:Todos|None = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo_authenticated(test_todos):
    request_data = {
        'title': 'new title new to update',
        'description': 'new description new to update',
        'priority': 5,
        'complete': False
    }

    response = client.put("/todos/todo/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestSessionLocal()
    model:Todos| None = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')

def test_update_todo_not_found_authenticated(test_todos):
    request_data = {
        'title': 'new title new to update',
        'description': 'new description new to update',
        'priority': 5,
        'complete': False
    }

    response = client.put("/todos/todo/999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail' : NOT_FOUND_DETAIL}

def test_delete_todo_authenticated(test_todos):
    response = client.delete("/todos/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found_authenticated(test_todos):
    response = client.delete("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': NOT_FOUND_DETAIL}

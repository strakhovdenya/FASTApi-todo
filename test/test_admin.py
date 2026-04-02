from starlette import status
from TodoApp.routers.auth import get_current_user
from TodoApp.routers.admin import get_db
from TodoApp.test.utils import *
from TodoApp.models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todos):
    resource = client.get("/admin/todo")
    assert resource.status_code == status.HTTP_200_OK
    assert resource.json() == [
        {'priority': 2,
         'id': 1,
         'title': 'learn code',
         'owner_id': 1,
         'description': 'learn code every day',
         'complete': False}
    ]

def test_admin_delete_authenticated(test_todos):
    response = client.delete("/admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_admin_delete_not_found_authenticated(test_todos):
    response = client.delete("/admin/todo/111")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'ToDo not found'}

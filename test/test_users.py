from starlette import status
from TodoApp.routers.auth import get_current_user
from TodoApp.routers.users import get_db
from TodoApp.test.utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todos):
    resource = client.get("/user")
    assert resource.status_code == status.HTTP_200_OK
    assert resource.json()['email'] == 'email@email.com'
    assert resource.json()['username'] == 'testuser'
    assert resource.json()['id'] == 1
    assert resource.json()['role'] == 'admin'
    assert resource.json()['first_name'] == 'Test'
    assert resource.json()['last_name'] == 'User'
    assert resource.json()['is_active'] == True
    assert resource.json()['phone_number'] is None



def test_change_password_authenticated(test_todos):
    resource = client.put("/user/password", json={"password": "qweqrrrqr", "new_password": "qweqrrrqr!!!new"})
    assert resource.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_current_password(test_todos):
    resource = client.put("/user/password", json={"password": "wrong_password", "new_password": "qweqrrrqr!!!new"})
    assert resource.status_code == status.HTTP_401_UNAUTHORIZED

def test_change_phone_number_authenticated(test_todos):
    resource = client.put("/user/phonenumber/111-111-1111", json={"password": "qweqrrrqr", "new_password": "qweqrrrqr!!!new"})
    assert resource.status_code == status.HTTP_204_NO_CONTENT
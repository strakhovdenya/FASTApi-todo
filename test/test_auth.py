from routers.auth import get_current_user, get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM
from test.utils import *
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_authenticate_user(test_todos):
    db = TestSessionLocal()

    authenticate_user_model = authenticate_user('testuser', 'qweqrrrqr', db)
    assert authenticate_user_model is not None
    assert 'testuser' == authenticate_user_model.username

    not_existing_user = authenticate_user('testuserwrond', 'qweqrrrqr', db)
    assert not_existing_user is False

    wrong_password_user = authenticate_user('testuser', 'wrong_pass', db)
    assert wrong_password_user is False


def test_create_user_token():
    username = 'testuser'
    user_id = 1
    role = 'admin'
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)
    decoded_token = jwt.decode(token, SECRET_KEY, ALGORITHM, options={'verify_signature': False})

    assert decoded_token['sub'] == username
    assert decoded_token['role'] == role
    assert decoded_token['id'] == user_id


@pytest.mark.asyncio
async def test_get_current_user():
    encode = {'sub': 'testuser', 'role': 'admin', 'id': 1}
    token = jwt.encode(encode, SECRET_KEY, ALGORITHM)

    user = await get_current_user(token)
    assert user == {'username': 'testuser', 'user_role': 'admin', 'id': 1}

@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'sub': 'testuser', 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, ALGORITHM)

    with pytest.raises(HTTPException) as ex:
        await get_current_user(token)

    assert ex.value.status_code == 401
    assert ex.value.detail == 'Could not validate credentials'
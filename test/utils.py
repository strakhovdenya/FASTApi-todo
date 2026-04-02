from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from ..database import Base
from fastapi.testclient import TestClient
import pytest
from ..main import app
from ..models import Todos, Users
from ..routers.users import bcrypt_context

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Ghbrjk12@localhost/TestTodoApplicationDatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URI, poolclass=StaticPool)

TestSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'testuser', 'id': 1, 'user_role': 'admin'}

client = TestClient(app)

hashed_password = bcrypt_context.hash('qweqrrrqr')

@pytest.fixture
def test_todos():
    user1 = Users(
        username='testuser',
        first_name='Test',
        last_name='User',
        hashed_password=hashed_password,
        email='email@email.com',
        role='admin'
    )

    todo = Todos(
        title='learn code',
        description='learn code every day',
        priority=2,
        complete=False,
        owner_id=1,
    )

    db = TestSessionLocal()
    db.add(user1)
    db.commit()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("delete from todos"))
        connection.execute(text("delete from users"))
        connection.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1;"))
        connection.execute(text("ALTER SEQUENCE todos_id_seq RESTART WITH 1;"))
        connection.commit()

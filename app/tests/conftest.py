import secrets
import time
import pytest

from validate import hash_password
from models import Base, User, get_engine, get_session_maker, Advertisement
from tests.config import ROOT_USER_EMAIL, ROOT_USER_PASSWORD


def get_random_password():
    password = secrets.token_hex()
    return f"{password[:10]}{password[10:20].upper()}"


@pytest.fixture(scope="session")
def root_user():
    return create_user(ROOT_USER_EMAIL, ROOT_USER_PASSWORD)


@pytest.fixture(scope="session", autouse=True)
def init_database():
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()


def create_user(email: str = None, password: str = None):
    email = email or f"user{time.time()}@email.te"
    password = password or get_random_password()
    Session = get_session_maker()
    with Session() as session:
        new_user = User(email=email, password=hash_password(password))
        session.add(new_user)
        session.commit()
        return {
            "id": new_user.id,
            "email": new_user.email,
            "password": password,
        }


@pytest.fixture()
def new_user():
    return create_user()


def create_adv(user: dict, title: str = None, description: str = None):
    title = title or f"advertisement{time.time()}"
    description = description or f"description{time.time()}"
    Session = get_session_maker()
    with Session() as session:
        new_adv = Advertisement(title=title, description=description, user_id=user['id'])
        session.add(new_adv)
        session.commit()
        return {
            "id": new_adv.id,
            "title": new_adv.title,
            "description": new_adv.description,
            "user_id": new_adv.user_id,
            "email": user['email'],
            "password": user['password']
        }


@pytest.fixture()
def new_adv(new_user):
    return create_adv(new_user)

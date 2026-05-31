# tests/conftest.py
import pytest
from app.factory import create_app
from app.dbhelper import db as _db
from app.models import User, UserRole, Game, Platform, Genre, Review
from app.config import Settings

@pytest.fixture(scope='session')
def app():
    """Создание экземпляра приложения для всей сессии тестов."""
    app = create_app(Settings(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
    ))
    return app

@pytest.fixture(scope='function')
def db(app):
    """Свежая чистая БД перед каждым тестом."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()

@pytest.fixture(scope='function')
def client(app, db):
    """Тестовый клиент Flask."""
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app, db):
    """Для запуска команд Flask CLI."""
    return app.test_cli_runner()

# Фикстуры для создания стандартных объектов
@pytest.fixture
def role_user(db):
    role = UserRole(name='user', value=0)
    db.session.add(role)
    db.session.commit()
    return role

@pytest.fixture
def role_admin(db):
    role = UserRole(name='admin', value=20)
    db.session.add(role)
    db.session.commit()
    return role

@pytest.fixture
def test_user(db, role_user):
    user = User(login='testuser', email='test@example.com', nickname='Test', role_id=role_user.id)
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def test_admin(db, role_admin):
    admin = User(login='admin', email='admin@example.com', nickname='Admin', role_id=role_admin.id)
    admin.set_password('adminpass')
    db.session.add(admin)
    db.session.commit()
    return admin

@pytest.fixture
def auth_client(client, test_user):
    """Клиент, уже авторизованный под test_user."""
    client.post('/auth/login', data={
        'login': 'testuser',
        'password': 'password'
    })
    return client

@pytest.fixture
def admin_client(client, test_admin):
    """Клиент, авторизованный под администратором."""
    client.post('/auth/login', data={
        'login': 'admin',
        'password': 'adminpass'
    })
    return client

@pytest.fixture(scope='function')
def genre(db):
    """Один жанр для тестов."""
    g = Genre(name='RPG')
    db.session.add(g)
    db.session.commit()
    return g

@pytest.fixture(scope='function')
def platform(db):
    """Одна платформа для тестов."""
    p = Platform(name='PC')
    db.session.add(p)
    db.session.commit()
    return p
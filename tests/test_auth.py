from app.crud.user_crud import get_user_by_login

def test_register(client, db):
    resp = client.post('/auth/register', data={
        'login': 'newuser',
        'email': 'new@test.com',
        'nickname': 'Newbie',
        'password': '123456',
        'password2': '123456'
    }, follow_redirects=True)
    assert resp.status_code == 200
    from app.models import User
    user = get_user_by_login('newuser')
    assert user is not None

def test_login_logout(client, test_user):
    # вход
    resp = client.post('/auth/login', data={
        'login': 'testuser',
        'password': 'password'
    }, follow_redirects=True)
    assert resp.status_code == 200
    # выход
    resp = client.get('/auth/logout', follow_redirects=True)
    assert resp.status_code == 200

def test_protected_page_redirects_guest(client, test_user):
    # Гость пытается попасть на страницу профиля test_user
    resp = client.get(f'/user/{test_user.id}/profile', follow_redirects=False)
    assert resp.status_code == 302
    assert '/auth/login' in resp.headers['Location']

def test_duplicate_registration(client, test_user):
    resp = client.post('/auth/register', data={
        'login': 'testuser',  # уже существует
        'email': 'another@test.com',
        'nickname': 'Test',
        'password': '123456',
        'password2': '123456'
    }, follow_redirects=True)
    assert 'Это имя уже занято' in resp.data.decode('utf-8')
from app.models import Review
from app.models import Game

def test_add_review(auth_client, db):
    game = Game(title='Для коментария')
    db.session.add(game)
    db.session.commit()
    resp = auth_client.post(f'/game/{game.id}/add_review', data={
        'mark': 4,
        'content': 'Пробую написать коментарий'
    }, follow_redirects=True)
    assert resp.status_code == 200
    review = db.session.scalar(db.select(Review).filter_by(game_id=game.id))
    assert review.mark == 4

def test_duplicate_review_fails(auth_client, db, test_user):
    game = Game(title='Для двух коментариев')
    db.session.add(game)
    db.session.commit()
    # первый отзыв
    auth_client.post(f'/game/{game.id}/add_review', data={
        'mark': 5, 'content': 'Мой первый коментарий'
    })
    # второй отзыв от того же пользователя
    resp = auth_client.post(f'/game/{game.id}/add_review', data={
        'mark': 3, 'content': 'Мой второй коментарий.'
    }, follow_redirects=True)
    assert 'Вы уже оставили отзыв на эту игру.' in resp.data.decode('utf-8')
    assert db.session.scalar(db.select(db.func.count()).select_from(Review).filter_by(game_id=game.id)) == 1

def test_guest_cannot_review(client, db):
    game = Game(title='Игра для гостя')
    db.session.add(game)
    db.session.commit()
    resp = client.post(f'/game/{game.id}/add_review', data={
        'mark': 3, 'content': 'Коментарий от гостя'
    }, follow_redirects=True)
    assert resp.status_code == 200

def test_banned_user_cannot_review(client, db, test_user):
    # баним пользователя
    test_user.banned = True
    db.session.commit()
    # логинимся
    client.post('/auth/login', data={
        'login': 'testuser', 'password': 'password'
    })
    game = Game(title='для забаненного')
    db.session.add(game)
    db.session.commit()
    resp = client.post(f'/game/{game.id}/add_review', data={
        'mark': 2, 'content': 'Меня забанили'
    }, follow_redirects=True)
    assert 'Ваш аккаунт заблокирован, вы не можете это сделать' in resp.data.decode('utf-8')
    assert db.session.scalar(db.select(db.func.count()).select_from(Review)) == 0
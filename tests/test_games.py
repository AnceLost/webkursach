from app.models.game import Game
from app.crud.game_crud import search_games
from app.models.platform import Platform
from app.models.genre import Genre

def test_admin_can_create_game(admin_client, db, platform, genre):
    resp = admin_client.post('/game/create', data={
        'title': 'New RPG',
        'description': 'Awesome game',
        'release_date': '2025-05-01',
        'platforms': [platform.id],
        'genres': [genre.id]
    }, follow_redirects=True)
    assert resp.status_code == 200
    game = search_games("New RPG").items[0] #индекс нужен, потому что search_games возвращает массив (с пагинацией)
    assert game is not None
    assert len(game.platforms) == 1
    assert game.platforms[0].name == 'PC'

def test_user_cannot_create_game(auth_client):
    resp = auth_client.post('/game/create', data={
        'title': 'Not allowed',
        'description': '...',
        'platforms': [1],
        'genres': [1]
    }, follow_redirects=True)
    # Должен быть 403
    assert resp.status_code == 403

def test_view_game_page(client, db, auth_client, genre, platform):
    game = Game(title='Public Game', description='Test')
    db.session.add(game)
    db.session.commit()
    resp = client.get(f'/game/{game.id}/profile')
    assert resp.status_code == 200
    assert 'Public Game' in resp.data.decode('utf-8')
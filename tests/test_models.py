import pytest
from app.models import User, Review, Game
from sqlalchemy.exc import IntegrityError

class TestUserModel:
    def test_password_hashing(self):
        u = User(login='u1', email='u1@t.com', nickname='U1')
        u.set_password('secret')
        assert u.password_hash != 'secret'
        assert u.check_password('secret') is True
        assert u.check_password('wrong') is False

    def test_default_role(self, test_user, role_user):
        assert test_user.role_id == role_user.id
        assert test_user.role.name == 'user'

    def test_banned_flag(self, test_user):
        assert test_user.banned == False
        test_user.banned = True
        assert test_user.banned == True

class TestReviewModel:
    def test_review_rating_range(self, db, test_user):
        game = Game(title='Range Game')
        db.session.add(game)
        db.session.commit()
        r = Review(mark=3, text='Ok', user=test_user, game=game)
        db.session.add(r)
        db.session.commit()  # должно пройти (check constraint от 1 до 5)
import io
from unittest.mock import patch
import pytest
from werkzeug.datastructures import FileStorage
from app.forms import RegistrationForm, ReviewForm, ImageForm


class TestRegistrationForm:
    @patch('app.forms.get_user_by_login', return_value=None)
    @patch('app.forms.get_user_by_email', return_value=None)
    def test_valid_data(self, mock_email, mock_login, app):
        with app.app_context():
            form = RegistrationForm(
                login='newuser', email='new@test.com', nickname='New',
                password='123456', password2='123456'
            )
            assert form.validate() == True
            mock_login.assert_called_once_with('newuser')
            mock_email.assert_called_once_with('new@test.com')

    @patch('app.forms.get_user_by_login', return_value=None)
    @patch('app.forms.get_user_by_email', return_value=None)
    def test_password_too_short(self, mock_email, mock_login, app):
        with app.app_context():
            form = RegistrationForm(
                login='newuser', email='new@test.com', nickname='New',
                password='123', password2='123'
            )
            assert form.validate() == False
            assert 'Пароль должен быть минимум 6 символов' in form.password.errors

    @patch('app.forms.get_user_by_login', return_value=None)
    @patch('app.forms.get_user_by_email', return_value=None)
    def test_passwords_mismatch(self, mock_email, mock_login, app):
        with app.app_context():
            form = RegistrationForm(
                login='newuser', email='new@test.com', nickname='New',
                password='123456', password2='654321'
            )
            assert form.validate() == False
            assert 'Пароли должны совпадать' in form.password2.errors

    @patch('app.forms.get_user_by_login', return_value=None)
    @patch('app.forms.get_user_by_email', return_value=None)
    def test_missing_login(self, mock_email, mock_login, app):
        with app.app_context():
            form = RegistrationForm(
                login='', email='a@b.com', nickname='N',
                password='123456', password2='123456'
            )
            assert form.validate() == False
            assert 'Логин обязателен' in form.login.errors
            # при пустом логине валидатор DataRequired останавливает цепочку,
            # поэтому get_user_by_login не должен вызываться
            mock_login.assert_not_called()


class TestReviewForm:
    def test_valid(self, app):
        with app.app_context():
            form = ReviewForm(mark=4, content='Достаточно длинный текст отзыва.')
            assert form.validate() == True

    def test_missing_rating(self, app):
        with app.app_context():
            form = ReviewForm(mark=None, content='Достаточно длинный текст.')
            assert form.validate() == False
            assert 'Это поле обязательно' in form.mark.errors


class TestImageForm:
    def test_valid_file(self, app):
        with app.app_context():
            fake_file = FileStorage(
                stream=io.BytesIO(b'fake image data'),
                filename='avatar.jpg',
                content_type='image/jpeg'
            )
            form = ImageForm(image=fake_file)
            assert form.validate() == True

    def test_invalid_extension(self, app):
        with app.app_context():
            fake_file = FileStorage(
                stream=io.BytesIO(b'fake data'),
                filename='avatar.txt',
                content_type='text/plain'
            )
            form = ImageForm(image=fake_file)
            assert form.validate() == False
            assert 'Только изображения' in form.image.errors[0]
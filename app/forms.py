import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, TextAreaField, SelectMultipleField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User
from crud.user_crud import get_user_by_login, get_user_by_email

class RegistrationForm(FlaskForm):
    login = StringField('Логин', validators=[
        DataRequired(message='Логин обязателен'),
        Length(min=3, max=64, message='Логин должен быть от 3 до 64 символов')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email обязателен'),
        Email(message='Введите корректный email')
    ])
    nickname = StringField('Отображаемое имя', validators=[
        DataRequired(message='Имя обязательно'),
        Length(min=3, max=64, message='Имя должно быть от 3 до 64 символов')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Пароль обязателен'),
        Length(min=6, message='Пароль должен быть минимум 6 символов')
    ])
    password2 = PasswordField('Повторите пароль', validators=[
        DataRequired(message='Подтверждение обязательно'),
        EqualTo('password', message='Пароли должны совпадать')
    ])
    submit = SubmitField('Зарегистрироваться')
    
    def validate_login(self, login):
        user = get_user_by_login(login.data)
        if user:
            raise ValidationError('Это имя уже занято.')
            
    def validate_email(self, email):
        user = get_user_by_email(email.data)
        if user:
            raise ValidationError('Этот email уже используется.')
        
class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(message="Введите логин")])
    password = PasswordField('Пароль', validators=[DataRequired(message="Введите пароль")])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    
def file_size_limit(form, field):
        MAX_SIZE = 5 * 1024 * 1024
        if field.data:
            if len(field.data.read()) > MAX_SIZE:
                # Сбрасываем указатель чтения файла обратно на 0
                field.data.seek(0)
                raise ValidationError('Файл слишком большой. Максимальный размер: 5 МБ')
            else:
                # Сбрасываем указатель, если файл прошел валидацию
                field.data.seek(0)    
    
class ImageForm(FlaskForm):
    image = FileField('Выберите изображение', validators=[])
    submit = SubmitField('Загрузить')

    def __init__(self, *validators, **kwargs):
        super().__init__(**kwargs)
        base = [
            file_size_limit,
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Только изображения (jpg, jpeg, png, gif)')
        ]
        self.image.validators = base + list(validators)
    
    
class ChangePasswordForm(FlaskForm):
    oldpass = PasswordField('Старый пароль', validators=[
        DataRequired(message='Для смены пароля нужно ввести старый'),
    ])
    newpass = PasswordField('Новый пароль', validators=[
        DataRequired(message='Пароль обязателен')
    ])
    newpass2 = PasswordField('Повторите новый пароль', validators=[
        DataRequired(message='Подтверждение обязательно'),
        EqualTo('newpass', message='Пароли должны совпадать')
    ])
    
    submit = SubmitField('Обновить')
    
class CreateGameForm(ImageForm):
    title = StringField('Название игры', validators=[
        DataRequired('Название игры обязательно'),
        Length(max=200)    
    ])
    description = TextAreaField('Описание')
    release_date = DateField('Дата релиза', default=datetime.date.today)
    platforms = SelectMultipleField('Платформы', coerce=int)
    genres = SelectMultipleField('Жанры', coerce=int)
    
class ReviewForm(FlaskForm):
    mark = SelectField('Оценка', 
                        choices=[(i, str(i)) for i in range(1, 6)], 
                        validators=[DataRequired('Это поле обязательно')], 
                        coerce=int)
    content = TextAreaField('Ваш отзыв', validators=[DataRequired(), Length(min=10, max=2000)])
    submit = SubmitField('Оставить отзыв')
    
class BanForm(FlaskForm):
    action = HiddenField('action', validators=[DataRequired()])
    submit = SubmitField('Забанить/Разбанить')
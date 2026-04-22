from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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
                raise ValidationError('Файл слишком большой. Максимальный размер: 1 МБ')
        # Сбрасываем указатель, если файл прошел валидацию
        field.data.seek(0)    
    
class AvatarForm(FlaskForm):
    avatar = FileField('Выберите изображение', validators=[
        FileRequired(message='Файл обязателен'),
        file_size_limit,
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Только изображения (jpg, jpeg, png, gif)')
    ])
    submit = SubmitField('Загрузить')
    
    
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required

from app.dbhelper import db
from app.models import User
from forms import RegistrationForm, LoginForm
from crud.user_crud import create_user, get_user, get_user_by_login

bp = Blueprint('auth', __name__, url_prefix='/auth')

def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Для доступа к данной странице необходимо пройти процедуру аутентификации.'
    login_manager.login_message_category = 'warning'
    login_manager.user_loader(load_user)
    login_manager.init_app(app)

def load_user(user_id):
    user = get_user(user_id)
    return user

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        if login and password:
            user = get_user_by_login(login)
            if user and user.check_password(password):
                login_user(user)
                flash('Вы успешно аутентифицированы.', 'success')
                next = request.args.get('next')
                return redirect(next or url_for('index'))
        flash('Введены неверные логин и/или пароль.', 'danger')
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            create_user(
                login = form.login.data,
                email = form.email.data,
                password = form.password.data,
                nickname =  form.nickname.data
                #это публичная форма регистрации, поэтому role_id подставится автоматически = 1
            )
            flash("Регистрация прошла успешно! Теперь войдите", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            app.logger.error(e)
            return "Произошла ошибка при регистрации", 500
    return render_template('auth/register.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
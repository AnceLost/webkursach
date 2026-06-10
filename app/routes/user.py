from pathlib import Path

from flask_login import current_user
from flask_wtf.file import FileRequired

from .base import *
from app.forms import ChangePasswordForm
from app.crud.user_crud import update_user_avatar, change_user_password, ban_user, unban_user, delete_user as du
from app.crud.review_crud import get_reviews_with_game 

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/<int:user_id>')
@login_required
@check_permissions(20) #20 - админ
def user_info(user_id):
    user = get_item(User, user_id)
    if(user):
        return render_template('user/info.html', user=user)

@bp.route('/<int:user_id>/profile')
@login_required
def profile(user_id):
    user = get_item(User, user_id)
    if not user:
        abort(404)
        
    selfprofile = True
    form = None
    delform = None
    adminMode = user.role.value >= 20
    
    if user_id != current_user.id:
        selfprofile = False
        
    if adminMode or selfprofile: 
        delform = DeleteForm()
        delform.submit.label.text = 'Удалить Пользователя'
        delform.submit.render_kw = {
                'class': 'btn btn-warning btn-sm',
                'onclick': "return confirm('Удалить пользователя? Все его отзывы будут удалены!');"
            }
    if adminMode:
        form = BanForm()
        if user.banned:
            form.action.data = 'unban'
            form.submit.label.text = 'Разбанить'
            form.submit.render_kw = {'class': 'btn btn-success btn-sm'}
        else:
            form.action.data = 'ban'
            form.submit.label.text = 'Забанить'
            form.submit.render_kw = {
                'class': 'btn btn-warning btn-sm',
                'onclick': "return confirm('Забанить пользователя? Все его отзывы будут удалены!');"
            }
    return render_template('user/profile.html', user=user, selfprofile=selfprofile, adminMode=adminMode, form=form, delform=delform)

@bp.route('/<int:user_id>/profile/personal-tierlist')
@login_required
def personal_tierlist(user_id):
    reviews = get_reviews_with_game(user_id)
    
    # границы для тиров
    tiers = {
        'S': 5,
        'A': 4,
        'B': 3,
        'C': 2,
        'D': 1
    }
    # Группируем отзывы по тирам
    tier_data = {}
    for tier, value in tiers.items():
        tier_data[tier] = [r for r in reviews if r.mark == value]

    return render_template('user/personal-tierlist.html', tier_data=tier_data)

@bp.route('/<int:user_id>/profile/change-avatar', methods=['GET', 'POST'])
@login_required
def change_avatar(user_id):
    user: User = get_item(User, user_id)
    if not user:
        abort(404)
    #аватарку может поменять модер, админ или сам пользователь
    if (current_user.id != user_id and current_user.role.value < 10):
        abort(403)  # доступ запрещён
        
    form = ImageForm(FileRequired(message='Файл обязателен'))
    avatar_path = None # необходимо определить заранее, чтобы везде была доступна
    if form.validate_on_submit():
        try:
            image = form.image.data
            avatar_path, avatar_filename = save_image(image, 'static/upload/avatars/', AvatarConverter())
            
            #берем старый путь до аватарки чтобы удалить, если обновление пройдет успешно
            oldfilepath = user.avatar_uri
            oldfilename = user.avatar_path
            
            update_user_avatar(user_id, avatar_filename)
            
            #Если код дошёл до сюда и не выдал ошибку, значит можно удалять старый аватар (если не стандартный)
            if oldfilename != 'defaultavatar.jpg':
                delete_image(oldfilepath)
            return redirect(url_for('user.profile', user_id=user_id))
            
        except FileSaveError as e:
            current_app.logger.error(f"Ошибка сохранения файла: {e}")
            flash('Не удалось сохранить новый аватар. Проверьте формат файла.', 'danger')
            # новый файл не создан, удалять нечего

        except DatabaseUpdateError as e:
            current_app.logger.error(f"Ошибка обновления профиля: {e}")
            # Удаляем только что сохранённый файл, т.к. БД не обновлена
            if avatar_path:
                try:
                    delete_image(avatar_path)
                except FileDeleteError as del_err:
                    current_app.logger.error(f"Не удалось удалить новый файл после ошибки БД: {del_err}")
            flash('Не удалось обновить аватар из-за ошибки базы данных.', 'danger')

        except FileDeleteError as e:
            # Старый файл не удалился, но новый уже в БД
            current_app.logger.error(f"Ошибка удаления старого аватара: {e}")
            flash('Аватар обновлён, но старый файл не был удалён. Администратор уведомлён.', 'warning')
            return redirect(url_for('user.profile', user_id=user_id))

        # Если мы здесь, значит была ошибка (кроме FileDeleteError, который уже сделал редирект)
        return render_template('user/change-avatar.html', form=form), 500

    return render_template('user/change-avatar.html', form=form)

@bp.route('/<int:user_id>/profile/change-pass', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    #пароль может поменять админ или сам пользователь
    if (current_user.id != user_id and current_user.role.value < 20):
        abort(403)  # доступ запрещён
    
    form = ChangePasswordForm()
    if form.validate_on_submit():
        oldpass = form.oldpass.data
        newpass = form.newpass.data
        if change_user_password(user_id, oldpass, newpass):
            flash('Пароль успешно изменен', 'success')
        else:
            flash('Не получилось поменять пароль, попробуйте позже или обратитесь к администратору', 'warning')
        return redirect(url_for('user.profile', user_id=user_id))
    return render_template('user/change-pass.html', form=form)

@bp.route('/<int:user_id>/toggle_ban', methods=['POST'])
@login_required
@check_permissions(20) #20 - админ
def toggle_ban(user_id):
    action = request.form.get('action')
    if action not in ('ban', 'unban'):
        abort(400, description="Неверное действие")
    try:
        if action=='ban': ban_user(user_id)
        elif action=='unban': unban_user(user_id)
    except DatabaseUpdateError as e:
        flash("Не удалось забанить/разбанить пользователя", 'danger')
        current_app.logger.error(e)
    return redirect(url_for('user.profile', user_id=user_id))

@bp.route('/<int:user_id>/delete', methods=["POST"])
@login_required
def delete_user(user_id: int):
    if current_user.role.value < 20 and current_user.id != user_id:
        abort(403)
    try:
        du(user_id)
    except DatabaseDeleteEntityError as e:
        flash(e)
    return redirect(url_for('index'))
    
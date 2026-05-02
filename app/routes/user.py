from pathlib import Path

from .base import *
from flask_login import current_user
from app.forms import ChangePasswordForm
from app.crud.user_crud import update_user_avatar, change_user_password
from app.crud.review_crud import get_reviews_with_game 
from flask_wtf.file import FileRequired


bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/<int:user_id>')
@login_required
def user_info(user_id):
    user = get_item(User, user_id)
    if(user):
        return render_template('user/info.html', user=user)

@bp.route('/<int:user_id>/profile')
@login_required
def profile(user_id):
    selfprofile = True
    user = current_user
    if user.id != user_id:
        user = get_item(User, user_id)
        selfprofile = False
    
    return render_template('user/profile.html', user=user, selfprofile=selfprofile)

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

@bp.route('profile/change-avatar', methods=['GET', 'POST'])
@login_required
def change_avatar():
    form = ImageForm(FileRequired(message='Файл обязателен'))
    avatar_path = None # необходимо определить заранее, чтобы везде была доступна
    if form.validate_on_submit():
        try:
            image = form.image.data
            avatar_path, avatar_filename = save_image(image, 'static/upload/avatars/', AvatarConverter())
            
            #берем старый путь до аватарки чтобы удалить, если обновление пройдет успешно
            oldfilepath = current_user.avatar_uri
            oldfilename = Path(oldfilepath).stem
            
            update_user_avatar(current_user.id, avatar_filename)
            
            #Если код дошёл до сюда и не выдал ошибку, значит можно удалять старый аватар (если не стандартный)
            if oldfilename != 'defaultavatar.jpg':
                delete_image(oldfilepath)
                
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
            return redirect(url_for('user.profile', user_id=current_user.id))

        # Если мы здесь, значит была ошибка (кроме FileDeleteError, который уже сделал редирект)
        return render_template('user/change-avatar.html', form=form), 500

    return render_template('user/change-avatar.html', form=form)

@bp.route('/profile/change-pass', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        oldpass = form.oldpass.data
        newpass = form.newpass.data
        if change_user_password(current_user.id, oldpass, newpass):
            flash('Пароль успешно изменен', 'success')
        else:
            flash('Не получилось поменять пароль, попробуйте позже или обратитесь к администратору', 'warning')
        return redirect(url_for('user.profile'))
    return render_template('user/change-pass.html', form=form)
from .base import *
from flask_login import current_user
from app.forms import AvatarForm

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/<int:user_id>')
@login_required
def user_info(user_id):
    user = get_user(user_id)
    if(user):
        return render_template('user/user_info.html', user=user)

@bp.route('/profile')
@login_required
def profile():
    return render_template('user/user_profile.html', user=current_user)

@bp.route('/profile/personal-tierlist')
@login_required
def personal_tierlist():
    return "заглушка для тирлиста", 200

@bp.route('profile/change-avatar')
@login_required
def change_avatar():
    form = AvatarForm()
    if form.validate_on_submit():
        try:
            # avatar_filename = save_avatar(form.avatar.data, old_filename=current_user.avatar_filename)
            # Обновляем поле в базе данных
            update_user_avatar(current_user.id, avatar_filename)
        except Exception as e:
            app.logger.error(e)
            return "Не получилось изменить аватарку", 500
        
        flash('Аватар успешно обновлён!', 'success')
        return redirect(url_for('user.profile'))  # или обратно на страницу профиля

    return render_template('user/change-avatar.html', form=form)
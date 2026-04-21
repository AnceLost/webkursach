from .base import *
from flask_login import current_user

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/<int:user_id>')
@login_required
def get_user(user_id):
    user = get_user(user_id)
    if(user):
        return render_template('user/user_info.html')

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
    pass
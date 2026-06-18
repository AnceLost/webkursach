from .base import *
from crud.access_log_crud import get_access_logs_time_desc

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@login_required
@check_permissions(20)
def dashboard():
    return render_template('admin/dashboard.html')

@bp.route('/users')
@login_required
@check_permissions(2)
def users():
    all_users = get_items(User, page=1, per_page=200)
    delform = DeleteForm()
    return render_template('admin/users.html', users=all_users, delform=delform)

@bp.route('/games')
@login_required
@check_permissions(2)
def games():
    all_games = get_items(Game, page=1, per_page=200)
    return render_template('admin/games.html', games=all_games)

@bp.route('/genres')
@login_required
@check_permissions(2)
def genres():
    all_genres = get_items(Genre, page=1, per_page=200)
    create_form = GenreForm()
    edit_form = GenreForm()
    delete_form = DeleteForm()
    return render_template('admin/genres.html',
                           genres=all_genres,
                           create_form=create_form,
                           edit_form=edit_form,
                           delete_form=delete_form)

@bp.route('/platforms')
@login_required
@check_permissions(2)
def platforms():
    all_platforms = get_items(Platform, page=1, per_page=200)
    create_form = PlatformForm()
    edit_form = PlatformForm()
    delete_form = DeleteForm()
    return render_template('admin/platforms.html',
                           platforms=all_platforms,
                           create_form=create_form,
                           edit_form=edit_form,
                           delete_form=delete_form)

@bp.route('/access_log')
@login_required
@check_permissions(2)
def access_log():
    logs = get_access_logs_time_desc().items
    return render_template('admin/access_log.html', logs=logs)
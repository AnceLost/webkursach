from .base import *
from app.crud.genre_crud import create_genre, edit_genre

bp = Blueprint('genre', __name__, url_prefix='/genre')

@bp.route('/create', methods=['POST'])
@login_required
@check_permissions(20)
def create():
    form = GenreForm()
    if form.validate_on_submit():
        try:
            genre = create_genre(name=form.name.data)
        except DatabaseCreateEntityError as e:
            flash('Ну удалось добавить жанр', 'danger')
            current_app.logger.error(f"Ошибка создания жанра: {e}")
        finally:   
            return redirect(url_for('admin.genres'))
    flash('Неправильный запрос (не через форму)')
    return redirect(url_for('admin.genres'))

@bp.route('/<int:genre_id>/edit', methods=['POST'])
@login_required
@check_permissions(20)
def edit(genre_id: int):
    form = GenreForm()
    if form.validate_on_submit():
        try:
            edit_genre(genre_id=genre_id, new_name=form.name.data)
        except DatabaseUpdateError as e:
            flash(f'Ну удалось обновить жанр <{genre_id}>', 'danger')
            current_app.logger.error(f"Ошибка обновления жанра<{genre_id}>: {e}")
        finally: 
            return redirect(url_for('admin.genres'))
    flash('Неправильный запрос (не через форму)')
    return redirect(url_for('admin.genres'))

@bp.route('/<int:genre_id>/delete', methods=['POST'])
@login_required
@check_permissions(20)
def delete(genre_id: int):
    form = DeleteForm()
    if form.validate_on_submit():
        try:
            delete_item(Genre, genre_id)
        except DatabaseDeleteEntityError as e:
            flash(f'Ну удалось удалить жанр <{genre_id}>', 'danger')
            current_app.logger.error(f"Ошибка удаления жанра<{genre_id}>: {e}")
        finally:
            return redirect(url_for('admin.genres'))
    flash('Неправильный запрос (не через форму)')
    return redirect(url_for('admin.genres'))
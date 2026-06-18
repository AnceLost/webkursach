from .base import *
from app.crud.platform_crud import create_platform, edit_platform

bp = Blueprint('platform', __name__, url_prefix='/platform')

@bp.route('/create', methods=['POST'])
@login_required
@check_permissions(20)
def create():
    form = PlatformForm()
    if form.validate_on_submit():
        try:
            platform = create_platform(name=form.name.data)
        except DatabaseCreateEntityError as e:
            flash('Ну удалось добавить платформу', 'danger')
            current_app.logger.error(f"Ошибка создания платформы: {e}")
        finally:
            return redirect(url_for('admin.platforms'))
    flash('Неправильный запрос (не через форму)')
    return redirect(url_for('admin.platforms'))

@bp.route('/<int:platform_id>/edit', methods=['POST'])
@login_required
@check_permissions(20)
def edit(platform_id: int):
    form = PlatformForm()
    if form.validate_on_submit():
        try:
            edit_platform(platform_id=platform_id, new_name=form.name.data)
        except DatabaseUpdateError as e:
            flash(f'Ну удалось обновить платформу <{platform_id}>', 'danger')
            current_app.logger.error(f"Ошибка обновления платформы<{platform_id}>: {e}")
        finally:
            return redirect(url_for('admin.platforms'))
    flash('Неправильный запрос (не через форму)')
    return redirect(url_for('admin.platforms'))

@bp.route('/<int:platform_id>/delete', methods=['POST'])
@login_required
@check_permissions(20)
def delete(platform_id: int):
    form = DeleteForm()
    if form.validate_on_submit():
        try:
            delete_item(Platform, platform_id)
        except DatabaseDeleteEntityError as e:
            flash(f'Ну удалось удалить платформу <{platform_id}>', 'danger')
            current_app.logger.error(f"Ошибка удаления платформы<{platform_id}>: {e}")
        finally:
            return redirect(url_for('admin.platforms'))
    flash('Неправильный запрос (не через форму)')
    return redirect(url_for('admin.platforms'))
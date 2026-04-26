from pathlib import Path

from flask_login import current_user

from .base import *
from app.crud.game_crud import create_game as cg


bp = Blueprint('game', __name__, url_prefix='/game')

@bp.route('/<int:game_id>')
@login_required
def game_info(game_id):
    game = get_item(Game, game_id)
    if game:
        return render_template('game/info.html', game=game)
    
@bp.route('/create')
@login_required
def create_game():
    form = CreateGameForm()
    platforms = [(p.id, p.name) for p in get_platforms()]
    genres = [(g.id, g.name) for g in get_genres()]
    
    form.platforms.choices = platforms
    form.genres.choices = genres
    
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        release_date = form.release_date.data
    
        selected_platforms = get_items_by_ids(Platform, form.platforms.data)
        selected_genres = get_items_by_ids(Genre, form.genres.data)   

        try:
            image = form.image.data
            cover_path, cover_filename = save_image(image, 'static/upload/covers/', AvatarConverter())
            game = cg(
                title=title,
                description=description,
                release_date=release_date,
                cover_path = cover_path,
                platforms=selected_platforms,
                genres=selected_genres
            )
            redirect(url_for('game.profile'))
        except FileSaveError as e:
            current_app.logger.error(f"Ошибка сохранения файла: {e}")
            flash('Не удалось сохранить обложку игры. Проверьте формат файла.', 'danger')
            # новый файл не создан, удалять нечего

        except DatabaseCreateEntityError as e:
            current_app.logger.error(f"Ошибка создания игры: {e}")
            # Удаляем только что сохранённый файл, т.к. БД не обновлена
            if cover_path:
                try:
                    delete_image(cover_path)
                except FileDeleteError as del_err:
                    current_app.logger.error(f"Не удалось удалить новый файл после ошибки БД: {del_err}")
            flash('Не удалось создать игру из-за ошибки базы данных.', 'danger')
        
        return redirect(url_for('game.create_game'))
    
    return render_template('game/create.html', form=form)
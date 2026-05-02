from pathlib import Path

from flask_login import current_user

from .base import *
from app.crud.game_crud import create_game as cg
from app.crud.review_crud import create_review, get_self_review


bp = Blueprint('game', __name__, url_prefix='/game')

@bp.route('/<int:game_id>')
@login_required
def game_info(game_id):
    game = get_item(Game, game_id)
    if game:
        return render_template('game/info.html', game=game)
    
@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateGameForm()
    platforms = [(p.id, p.name) for p in get_items(Platform, per_page=200)] # больше 200 врядли наберется
    genres = [(g.id, g.name) for g in get_items(Genre, per_page=200)] # больше 200 врядли наберется
    
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
            cover_filename = None
            if image:
                cover_path, cover_filename = save_image(image, 'static/upload/covers/', AvatarConverter())
            game = cg(
                title=title,
                description=description,
                release_date=release_date,
                cover_path=cover_filename,
                platforms=selected_platforms,
                genres=selected_genres
            )
            return redirect(url_for('game.profile', game_id=game.id))
        
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
        
        return redirect(url_for('game.create'))
    
    return render_template('game/create.html', form=form)

@bp.route('/<int:game_id>/profile', methods=['GET', 'POST'])
def profile(game_id):
    game = get_item(Game, game_id)
    if game is None:
        abort(404)
    form = ReviewForm()
    
    # Проверяем, оставил ли текущий пользователь уже отзыв
    user_review = None
    if current_user.is_authenticated:
        user_review = get_self_review(current_user.id, game_id)
        
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Войдите, чтобы оставить отзыв.', 'warning')
            return redirect(url_for('auth.login'))

        if user_review:
            flash('Вы уже оставили отзыв на эту игру.', 'warning')
            return redirect(url_for('game.profile', game_id=game_id))
        
        mark = form.mark.data
        content = form.content.data
        try:
            review = create_review(
                mark=mark,
                content=content,
                user_id=current_user.id,
                game_id=game_id
            )
        except DatabaseCreateEntityError as e:
            flash('Не удалось оставить коментарий', 'warning')
            print(e)
        return redirect(url_for('game.profile', game_id=game_id))

    page = request.args.get('page', 1, type=int)    
    reviews = get_items(Review, page=page, per_page=5)
    return render_template('game/profile.html', 
                           game=game, 
                           reviews=reviews, 
                           user_review=user_review, 
                           form=form,
                           page=page,
                           max_page=int(len(reviews)/5) + 1)
    
@bp.route('/search')
def search():
    pass
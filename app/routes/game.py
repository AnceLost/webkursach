from pathlib import Path

from flask_login import current_user

from .base import *
from app.crud.game_crud import create_game as cg, search_games, delete_game as delete_game_crud
from app.crud.review_crud import create_review, get_self_review, get_pagination_reviews_for_games


bp = Blueprint('game', __name__, url_prefix='/game')

@bp.route('/<int:game_id>')
@login_required
@check_permissions(20) #20 - админ
def game_info(game_id):
    game = get_item(Game, game_id)
    if game:
        return render_template('game/info.html', game=game)
    
@bp.route('/create', methods=['GET', 'POST'])
@login_required
@check_permissions(10) #10 - модератор и выше
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

@bp.route('/<int:game_id>/profile', methods=['GET'])
def profile(game_id):
    game = get_item(Game, game_id)
    if game is None:
        abort(404)
    form = ReviewForm()
    
    adminMode = False
    deleteForm = None
    # Проверяем, оставил ли текущий пользователь уже отзыв
    user_review = None
    if current_user.is_authenticated:
        user_review = get_self_review(current_user.id, game_id)
        if current_user.role.value >= 20:
            adminMode = True
            deleteForm = DeleteForm()

    page = request.args.get('page', 1, type=int)    
    reviews = get_pagination_reviews_for_games(game_id, page=page, per_page=5)
    banned = current_user.banned if current_user.is_authenticated else False
    return render_template('game/profile.html', 
                           game=game, 
                           reviews=reviews, 
                           user_review=user_review, 
                           form=form,
                           page=page,
                           has_next_page=reviews.has_next,
                           user_has_banned=banned,
                           adminMode=adminMode,
                           deleteForm=deleteForm)

@bp.route('/<int:game_id>/add_review', methods=['POST'])
@login_required
@check_not_banned
def add_review(game_id: int):
    game = get_item(Game, game_id)
    if game is None:
        abort(404)
        
    form = ReviewForm()
    
    if form.validate_on_submit():
        user_review = get_self_review(current_user.id, game_id)
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
    
    return redirect(url_for('game.profile', game_id=game_id))

@bp.route('/<int:game_id>/delete_review/<int:review_id>', methods=['POST'])
def delete_review(game_id:int, review_id: int):
    review = get_item(Review, review_id)
    if review is None:
        abort(404)

    if not (current_user.id == review.user_id or current_user.role.value >= 20):
        abort(403)    
        
    try:
        delete_item(Review, review_id)
    except DatabaseDeleteEntityError as e:
        current_app.logger.error(f"Не получилось удалить коментарий: {e}")
        flash('Не получилось удалить коментарий', 'danger')
    return redirect(url_for('game.profile', game_id=game_id))
    
@bp.route('/search')
def search():
    title_query = request.args.get('q', '').strip()
    genre_ids_str = request.args.getlist('genres')  # поддерживает множественные параметры ?genres=1&genres=2
    page = request.args.get('page', 1, type=int)

    # Преобразуем строковые id в целые
    genre_ids = []
    for gid in genre_ids_str:
        try:
            genre_ids.append(int(gid))
        except ValueError:
            pass

    games = search_games(
        title_contains=title_query if title_query else None,
        genre_ids=genre_ids if genre_ids else None,
        page=page,
        per_page=20
    )

    # Для отображения фильтра жанров передадим все жанры
    all_genres = get_items(Genre, per_page=100)

    return render_template(
        'game/search.html',
        games=games,
        title_query=title_query,
        selected_genre_ids=genre_ids,
        all_genres=all_genres,
        page=page
    )
    
@bp.route('/<int:game_id>/delete', methods=["POST"])
@login_required
@check_permissions(20)
def delete_game(game_id: int):
    game = get_item(Game, game_id)
    if game is None:
        abort(404)
        
    try:
        delete_game_crud(game_id)
    except DatabaseDeleteEntityError as del_err:
        current_app.logger.error(f"Не получилось удалить игру: {del_err}")
        flash('Не получилось удалить игру', 'danger')
    return redirect(url_for('index'))    
    
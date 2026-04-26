from pathlib import Path

from flask_login import current_user

from .base import *
from app.crud.game_crud import get_game
bp = Blueprint('game', __name__, url_prefix='/game')

@bp.route('/<int:game_id>')
@login_required
def game_info(game_id):
    game = get_game(game_id)
    if game:
        return render_template('game/game_info.html', game=game)
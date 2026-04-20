from flask import (
    Flask, request, session, 
    url_for, redirect, render_template, 
    flash, make_response, Blueprint)
from crud.user_crud import get_user
from .base import login_required

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/<int:user_id>')
@login_required
def get_user(user_id):
    user = get_user(user_id)
    if(user):
        return render_template('user/user_info.html')
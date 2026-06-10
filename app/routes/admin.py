from .base import *

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('')
@login_required
@check_permissions(20)
def index():
    return render_template('admin/index.html')
import os

from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required
from flask import (
    Flask, request, session, 
    url_for, redirect, render_template, 
    flash, make_response, Blueprint, current_app)


from app.crud.user_crud import get_user
from app.utils import AvatarConverter, save_image, delete_image
from app.exceptions import ApplicationError, FileDeleteError, FileSaveError, DatabaseUpdateError

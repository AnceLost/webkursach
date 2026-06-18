import os

from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required
from flask import (
    Flask, request, session, 
    url_for, redirect, render_template, 
    flash, make_response, Blueprint, current_app, abort)

from app.models import User, Game, Platform, Genre, Review
from app.crud.base import get_item, get_items, get_items_by_ids, delete_item
from app.forms import ImageForm, CreateGameForm, ReviewForm, BanForm, DeleteForm, GenreForm, PlatformForm
from app.utils import AvatarConverter, save_image, delete_image, check_permissions, check_not_banned
from app.exceptions import (ApplicationError, 
                            FileDeleteError, 
                            FileSaveError, 
                            DatabaseUpdateError, 
                            DatabaseError,
                            DatabaseCreateEntityError,
                            DatabaseDeleteEntityError,
                            DatabaseNotFoundError)
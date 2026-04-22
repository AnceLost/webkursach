from flask_login import LoginManager, login_user, logout_user, login_required
from flask import (
    Flask, request, session, 
    url_for, redirect, render_template, 
    flash, make_response, Blueprint)
from crud.user_crud import get_user, update_user_avatar

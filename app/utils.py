import os
import secrets
from typing import Callable
from functools import wraps

from PIL import Image
from flask import current_app, redirect, url_for, abort, flash
from flask_login import current_user

from app.exceptions import FileSaveError, FileDeleteError

class Converter:
    
    def proceed(self, img: Image) -> Image:
        return img
    
class AvatarConverter(Converter):
    
    def __init__(self, output_size: tuple[int, int] = (300,300)):
        self.output_size = output_size
    
    def proceed(self, img: Image) -> Image:
        # Конвертируем RGBA в RGB, если есть альфа-канал
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            # Создаём белый фон для прозрачных областей
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        else:
            img = img.convert('RGB')
        img.thumbnail(self.output_size)
        return img

def save_image(image, path_to_img_dir: str, converter: Converter = None) -> [str, str]:
    """
    Сохраняет загруженное изображение, изменяет размер, возвращает имя файла.
    :param image: Входное изображение
    :param path_to_img_dir: Путь до директории с картинками типа static/upload/...
    :param converter: Можно передать любой ковертер, у которого реализован метод proceed
    :return: Имя файла (без пути)
    """
    try:
        # Генерируем случайное имя файла, чтобы избежать коллизий
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(image.filename)
        image_fn = random_hex + f_ext

        # Полный путь для сохранения
        image_path = os.path.join(current_app.root_path, path_to_img_dir, image_fn)

        # Обработка изображения
        
        img = Image.open(image)
        if converter: img = converter.proceed(img)
        img.save(image_path, 'JPEG', quality=85)  # сохраняем как JPEG для единообразия

        return image_path, image_fn
    except Exception as e:
        raise FileSaveError(f"Не удалось сохранить изображение: {e}") from e

def delete_image(file_path: str):
    """Удаляет файл"""
    file_path = file_path.lstrip('/') #убирает первый слэш в начале пути
    file_path = os.path.join(current_app.root_path, file_path)
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except OSError as e:
            raise FileDeleteError(f"Не получилось удалить {file_path}") from e

#декоратор для проверки уровня доступа
def check_permissions(required_access_level: int):
    def wrapper(func: Callable):
        @wraps(func)
        def inner(*args, **kwargs):
            nonlocal required_access_level #иначе не видит 
            access_level = current_user.role.value
            if access_level < required_access_level:
                abort(403)  # доступ запрещён
            res = func(*args, **kwargs)
            return res
        return inner
    return wrapper

#декоратор для проверки бана
def check_not_banned(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.banned:
            flash("Ваш аккаунт заблокирован, вы не можете это сделать", 'danger')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return wrapper

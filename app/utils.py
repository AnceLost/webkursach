import os
import secrets
from PIL import Image

def save_avatar(avatar_picture):
    # Генерируем случайное имя файла
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    avatar_fn = random_hex + f_ext
    
    # Путь для сохранения внутри static
    avatar_path = os.path.join(current_app.root_path, 'static/uploads/avatars', avatar_fn)
    
    # Изменяем размер изображения (опционально)
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(avatar_path)
    
    # Возвращаем относительный путь для БД
    return f'uploads/avatars/{avatar_fn}'
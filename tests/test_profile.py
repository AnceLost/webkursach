import io
import os

from unittest.mock import patch
from PIL import Image as PILImage

from app.models import User
from app.crud.base import get_item

def test_avatar_upload(auth_client, app, db, test_user, tmp_path):
    # патчим корень приложения для сохранения файлов в tmp_path
    avatar_dir = tmp_path / 'static' / 'upload' / 'avatars'
    avatar_dir.mkdir(parents=True, exist_ok=True)
    default_avatar = avatar_dir / 'defaultavatar.jpg'
    default_avatar.write_text('default')

    # тестовая картинка, чтобы Pillow без ошибок открыл её
    img = PILImage.new('RGB', (1, 1), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    fake_file = (img_bytes, 'test_avatar.jpg')

    with patch('app.utils.current_app.root_path', new=str(tmp_path)):
        data = {
            'image': fake_file,
            'submit': 'Загрузить'
        }
        resp = auth_client.post(
            f'user/{test_user.id}/profile/change-avatar',
            data=data,
            content_type='multipart/form-data',
            follow_redirects=True
        )
        assert resp.status_code == 200
        # имя файла должно измениться
        user = get_item(User, test_user.id)
        assert user.avatar_path != 'defaultavatar.jpg'
        # также нужно убедиться, что файл есть сам по себе
        new_file = avatar_dir / user.avatar_path
        assert new_file.exists()

def test_change_password(auth_client, test_user):
    resp = auth_client.post(f'/user/{test_user.id}/profile/change-pass', data={
        'oldpass': 'password',
        'newpass': 'newpassword',
        'newpass2': 'newpassword'
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert 'Пароль успешно изменен' in resp.data.decode('utf-8')
class ApplicationError(Exception):
    """Базовое исключение приложения."""
    pass

class FileSaveError(ApplicationError):
    """Ошибка сохранения файла."""
    pass

class FileDeleteError(ApplicationError):
    """Ошибка удаления файла."""
    pass

class DatabaseError(ApplicationError):
    """Базовая ошибка при взаимодействии с БД"""
    pass

class DatabaseUpdateError(DatabaseError):
    """Ошибка обновления базы данных."""
    pass

class DatabaseNotFoundError(DatabaseError):
    """Ошибка при запросе несуществующего"""
    pass

class DatabaseCreateEntityError(DatabaseError):
    """Ошибка при создании какого-то объекта(-ов) в базе"""
    pass
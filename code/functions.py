import os
import sys
import shutil


def resource_path(relative_path):
    # Возвращает абсолютный путь к ресурсу
    base_path = getattr(sys, "_MEIPASS", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    return os.path.normpath(os.path.join(base_path, relative_path))


def get_database_path():
    # функция получения пути до базы данных
    resource_db_path = resource_path("For_database/records.sqlite")

    if not getattr(sys, "_MEIPASS", None):
        return resource_db_path

    exe_dir = os.path.dirname(sys.executable)
    db_path = os.path.join(exe_dir, "records.sqlite")

    if not os.path.exists(db_path):
        try:
            shutil.copy2(resource_db_path, db_path)
        except Exception:
            return resource_db_path

    return db_path

import os
import sys
import shutil
from constants import MODIFY_FILES


def resource_path(relative_path):
    # Возвращает абсолютный путь к ресурсу
    base_path = getattr(sys, "_MEIPASS", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    return os.path.normpath(os.path.join(base_path, relative_path))


def get_path(file="db"):
    # функция получения пути до базы данных
    correct_path = resource_path(MODIFY_FILES[file][0])

    if not getattr(sys, "_MEIPASS", None):
        return correct_path

    exe_dir = os.path.dirname(sys.executable)
    path = os.path.join(exe_dir, MODIFY_FILES[file][1])

    if not os.path.exists(path):
        try:
            shutil.copy2(correct_path, path)
        except Exception:
            return correct_path

    return path

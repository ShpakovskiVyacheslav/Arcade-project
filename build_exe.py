import os
from pathlib import Path

import PyInstaller.__main__

PROJECT_ROOT = Path(__file__).resolve().parent
CODE_DIR = PROJECT_ROOT / "code"


def data_option(source: Path, target):
    return f"{source}{os.pathsep}{target}"


def main():
    PyInstaller.__main__.run([
        str(CODE_DIR / "main.py"),
        "--name=Fish_hunter",
        "--noconfirm",
        "--clean",
        "--windowed",
        "--onefile",
        "--distpath",
        str(PROJECT_ROOT / "dist"),
        "--workpath",
        str(PROJECT_ROOT / "build"),
        "--specpath",
        str(PROJECT_ROOT / "build"),
        "--paths",
        str(CODE_DIR),
        "--hidden-import=arcade",
        "--hidden-import=arcade.gui",
        "--hidden-import=arcade.key",
        "--hidden-import=arcade.color",
        "--hidden-import=pyglet",
        "--hidden-import=PIL",
        "--hidden-import=PIL.Image",
        "--hidden-import=backports.tarfile",
        "--hidden-import=jaraco.text",
        "--hidden-import=jaraco.context",
        "--add-data",
        data_option(PROJECT_ROOT / "settings" / "settings.json", "settings"),
        "--add-data",
        data_option(PROJECT_ROOT / "static", "static"),
        "--add-data",
        data_option(PROJECT_ROOT / "for_database" / "records.sqlite", "for_database")
    ])


if __name__ == "__main__":
    main()

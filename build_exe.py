import os
from pathlib import Path

import PyInstaller.__main__


PROJECT_ROOT = Path(__file__).resolve().parent
CODE_DIR = PROJECT_ROOT / "Code"


def data_option(source: Path, target):
    return f"{source}{os.pathsep}{target}"


def main():
    PyInstaller.__main__.run(
        [
            str(CODE_DIR / "main.py"),
            "--name=Fish hunter",
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
            "--add-data",
            data_option(PROJECT_ROOT / "static", "static"),
            "--add-data",
            data_option(PROJECT_ROOT / "For_database" / "records.sqlite", "For_database"),
        ]
    )


if __name__ == "__main__":
    main()


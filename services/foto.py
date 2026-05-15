import os
import shutil
import datetime

from PySide6.QtGui import QPixmap

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOTOS_DIR = os.path.join(BASE_DIR, "assets", "fotos")

os.makedirs(FOTOS_DIR, exist_ok=True)


def salvar_foto(origem):

    ext = os.path.splitext(origem)[1].lower()

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    destino = os.path.join(
        FOTOS_DIR,
        f"aluno_{ts}{ext}"
    )

    shutil.copy2(origem, destino)

    return destino


def carregar_foto(path):

    if not os.path.exists(path):
        return QPixmap()

    return QPixmap(path)
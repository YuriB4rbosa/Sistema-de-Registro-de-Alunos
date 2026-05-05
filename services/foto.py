import os
import shutil
import datetime
from PIL import Image, ImageTk, ImageDraw

BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOTOS_DIR = os.path.join(BASE_DIR, "assets", "fotos")
os.makedirs(FOTOS_DIR, exist_ok=True)


def salvar_foto(origem):
    
    ext     = os.path.splitext(origem)[1].lower()
    ts      = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    destino = os.path.join(FOTOS_DIR, f"aluno_{ts}{ext}")
    shutil.copy2(origem, destino)
    return destino


def carregar_foto_tk(path, tamanho=(110, 110), circular=True):
    
    img = Image.open(path).resize(tamanho, Image.LANCZOS)
    if circular:
        mask  = Image.new("L", tamanho, 0)
        ImageDraw.Draw(mask).ellipse((0, 0, *tamanho), fill=255)
        img_r = Image.new("RGBA", tamanho, (0, 0, 0, 0))
        img_r.paste(img.convert("RGBA"), mask=mask)
        return ImageTk.PhotoImage(img_r)
    return ImageTk.PhotoImage(img)
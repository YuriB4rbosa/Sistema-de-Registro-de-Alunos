from tkinter import ttk


TEMA_CLARO = {
    "AZUL_ESCURO": "#042C53",
    "AZUL_MEDIO":  "#185FA5",
    "AZUL_CLARO":  "#E6F1FB",
    "AZUL_BORDA":  "#B5D4F4",
    "BRANCO":      "#FFFFFF",
    "CINZA_BG":    "#F5F4F1",
    "CINZA_CARD":  "#F1EFE8",
    "CINZA_BORDA": "#D3D1C7",
    "CINZA_TEXTO": "#5F5E5A",
    "CINZA_LABEL": "#888780",
    "PRETO_TEXTO": "#2C2C2A",
    "VERDE":       "#0F6E56",
    "VERDE_BG":    "#E1F5EE",
    "VERMELHO":    "#A32D2D",
    "VERMELHO_BG": "#FCEBEB",
    "CORAL":       "#993C1D",
    "CORAL_BG":    "#FAECE7",
    "AMARELO_BG":  "#FAEEDA",
    "AMARELO":     "#854F0B",
    "ROXO":        "#4A1D96",
    "ROXO_BG":     "#EDE9FE",
}


TEMA_ESCURO = {
    "AZUL_ESCURO": "#0D1B2A",
    "AZUL_MEDIO":  "#378ADD",
    "AZUL_CLARO":  "#1A2E42",
    "AZUL_BORDA":  "#2A4A6B",
    "BRANCO":      "#1E2530",
    "CINZA_BG":    "#141920",
    "CINZA_CARD":  "#1A2030",
    "CINZA_BORDA": "#2A3040",
    "CINZA_TEXTO": "#A0A8B4",
    "CINZA_LABEL": "#6A7480",
    "PRETO_TEXTO": "#E0E6F0",
    "VERDE":       "#1DB37A",
    "VERDE_BG":    "#0D2820",
    "VERMELHO":    "#E05555",
    "VERMELHO_BG": "#2A1515",
    "CORAL":       "#C06040",
    "CORAL_BG":    "#2A1A10",
    "AMARELO_BG":  "#2A2010",
    "AMARELO":     "#D4A030",
    "ROXO":        "#9060D0",
    "ROXO_BG":     "#1E1030",
}

# ── Estado global do tema ────────────────────────────────────────
_tema_atual = TEMA_CLARO.copy()


def _aplicar_tema(tema):
    global _tema_atual
    _tema_atual = tema.copy()
    
    import utils.estilos as _self
    for k, v in tema.items():
        setattr(_self, k, v)


def alternar_tema():
    
    import utils.estilos as _self
    if _self.BRANCO == TEMA_CLARO["BRANCO"]:
        _aplicar_tema(TEMA_ESCURO)
        return "escuro"
    else:
        _aplicar_tema(TEMA_CLARO)
        return "claro"


def tema_escuro_ativo():
    import utils.estilos as _self
    return _self.BRANCO != TEMA_CLARO["BRANCO"]



AZUL_ESCURO = TEMA_CLARO["AZUL_ESCURO"]
AZUL_MEDIO  = TEMA_CLARO["AZUL_MEDIO"]
AZUL_CLARO  = TEMA_CLARO["AZUL_CLARO"]
AZUL_BORDA  = TEMA_CLARO["AZUL_BORDA"]
BRANCO      = TEMA_CLARO["BRANCO"]
CINZA_BG    = TEMA_CLARO["CINZA_BG"]
CINZA_CARD  = TEMA_CLARO["CINZA_CARD"]
CINZA_BORDA = TEMA_CLARO["CINZA_BORDA"]
CINZA_TEXTO = TEMA_CLARO["CINZA_TEXTO"]
CINZA_LABEL = TEMA_CLARO["CINZA_LABEL"]
PRETO_TEXTO = TEMA_CLARO["PRETO_TEXTO"]
VERDE       = TEMA_CLARO["VERDE"]
VERDE_BG    = TEMA_CLARO["VERDE_BG"]
VERMELHO    = TEMA_CLARO["VERMELHO"]
VERMELHO_BG = TEMA_CLARO["VERMELHO_BG"]
CORAL       = TEMA_CLARO["CORAL"]
CORAL_BG    = TEMA_CLARO["CORAL_BG"]
AMARELO_BG  = TEMA_CLARO["AMARELO_BG"]
AMARELO     = TEMA_CLARO["AMARELO"]
ROXO        = TEMA_CLARO["ROXO"]
ROXO_BG     = TEMA_CLARO["ROXO_BG"]

# ── Fontes ───────────────────────────────────────────────────────
FONT_TITULO = ("Segoe UI", 11, "bold")
FONT_LABEL  = ("Segoe UI", 9)
FONT_ENTRY  = ("Segoe UI", 10)
FONT_BTN    = ("Segoe UI", 9, "bold")
FONT_TABELA = ("Segoe UI", 9)
FONT_MONO   = ("Consolas", 9)


def aplicar_estilo(root):
    
    import utils.estilos as e
    s = ttk.Style(root)
    s.theme_use("clam")
    s.configure("Treeview",
                background=e.BRANCO, foreground=e.PRETO_TEXTO,
                fieldbackground=e.BRANCO, rowheight=30,
                font=FONT_TABELA, borderwidth=0)
    s.configure("Treeview.Heading",
                background=e.CINZA_CARD, foreground=e.CINZA_LABEL,
                font=("Segoe UI", 8, "bold"), relief="flat")
    s.map("Treeview",
          background=[("selected", e.AZUL_CLARO)],
          foreground=[("selected", e.AZUL_ESCURO)])
    s.configure("Vertical.TScrollbar",
                background=e.CINZA_CARD, troughcolor=e.CINZA_BG,
                borderwidth=0, arrowsize=12)
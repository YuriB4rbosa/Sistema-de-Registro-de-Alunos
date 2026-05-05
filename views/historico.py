import tkinter as tk
from tkinter import ttk

from utils.estilos import (BRANCO, CINZA_BG, CINZA_BORDA, PRETO_TEXTO,
                            VERDE, AZUL_MEDIO, VERMELHO, FONT_TABELA)
from utils.widgets import make_scrolled_tree


class HistoricoView(tk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent, bg=CINZA_BG)
        self.db = db
        self._build()

    def _build(self):
        tk.Label(self, text="Histórico de alterações",
                 font=("Segoe UI", 14, "bold"),
                 bg=CINZA_BG, fg=PRETO_TEXTO).pack(anchor="w", pady=(0, 12))

        card = tk.Frame(self, bg=BRANCO, bd=1, relief="solid",
                        highlightthickness=1, highlightbackground=CINZA_BORDA)
        card.pack(fill="both", expand=True)

        self._tree = make_scrolled_tree(card,
            columns=("data","usuario","acao","id","nome","detalhes"),
            headings_cfg={
                "data":     ("Data/Hora",  130),
                "usuario":  ("Usuário",     90),
                "acao":     ("Ação",        80),
                "id":       ("ID",          40),
                "nome":     ("Aluno",      160),
                "detalhes": ("Detalhes",   280),
            })

        self._tree.tag_configure("CADASTRO",    foreground=VERDE)
        self._tree.tag_configure("ATUALIZAÇÃO", foreground=AZUL_MEDIO)
        self._tree.tag_configure("EXCLUSÃO",    foreground=VERMELHO)
        self._tree.tag_configure("PDF",         foreground="#4A1D96")

    def atualizar(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        for row in self.db.historico.listar():
            self._tree.insert("", "end", values=row, tags=(row[2],))
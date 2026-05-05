import tkinter as tk
from utils.estilos import (BRANCO, CINZA_BG, CINZA_CARD, CINZA_BORDA,
                            CINZA_LABEL, PRETO_TEXTO, AZUL_ESCURO,
                            AZUL_MEDIO, AZUL_CLARO, VERDE, VERDE_BG,
                            VERMELHO, CORAL, CORAL_BG, ROXO, ROXO_BG,
                            AMARELO, AMARELO_BG, FONT_MONO, FONT_LABEL)
from utils.widgets import make_card


class DashboardView(tk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent, bg=CINZA_BG)
        self.db = db
        self._build()

    def _build(self):
        tk.Label(self, text="Dashboard", font=("Segoe UI", 16, "bold"),
                 bg=CINZA_BG, fg=PRETO_TEXTO).pack(anchor="w", pady=(0, 14))

        # Cards de estatística
        stat_frame = tk.Frame(self, bg=CINZA_BG)
        stat_frame.pack(fill="x", pady=(0, 16))

        self._stat_labels = {}
        stats_cfg = [
            ("total",     "Total de Alunos",    AZUL_ESCURO, AZUL_CLARO,  "🎓"),
            ("masculino", "Masculino",           AZUL_MEDIO,  AZUL_CLARO,  "♂"),
            ("feminino",  "Feminino",            CORAL,       CORAL_BG,    "♀"),
            ("cursos",    "Cursos Diferentes",   VERDE,       VERDE_BG,    "📚"),
            ("idade",     "Idade Média",         ROXO,        ROXO_BG,     "📅"),
            ("novos",     "Cadastros Recentes",  AMARELO,     AMARELO_BG,  "✨"),
        ]
        for i, (key, label, cor, bg, icon) in enumerate(stats_cfg):
            card = tk.Frame(stat_frame, bg=bg, bd=1, relief="solid",
                            highlightthickness=1, highlightbackground=CINZA_BORDA)
            card.grid(row=0, column=i, padx=6, sticky="ew")
            stat_frame.columnconfigure(i, weight=1)
            tk.Label(card, text=icon, font=("Segoe UI", 18),
                     bg=bg, fg=cor).pack(pady=(14, 4))
            lbl = tk.Label(card, text="—", font=("Segoe UI", 22, "bold"),
                            bg=bg, fg=cor)
            lbl.pack()
            tk.Label(card, text=label, font=("Segoe UI", 8),
                     bg=bg, fg=cor, wraplength=100, justify="center").pack(pady=(2, 14))
            self._stat_labels[key] = lbl

        # Top cursos
        self._top_frame = make_card(self, "Top 10 cursos mais procurados", "📊")

        # Últimos alunos
        self._rec_frame = make_card(self, "Últimos alunos cadastrados", "🕓")

    def atualizar(self):
        total  = self.db.alunos.contar()
        sexos  = self.db.alunos.stats_por_sexo()
        cursos = self.db.alunos.stats_por_curso()
        idade  = self.db.alunos.media_idade()
        novos  = self.db.historico.novos_este_mes()

        self._stat_labels["total"].configure(text=str(total))
        self._stat_labels["masculino"].configure(text=str(sexos.get("M", 0)))
        self._stat_labels["feminino"].configure(text=str(sexos.get("F", 0)))
        self._stat_labels["cursos"].configure(text=str(len(cursos)))
        self._stat_labels["idade"].configure(text=f"{idade} a")
        self._stat_labels["novos"].configure(text=str(novos))

        # Barras de cursos
        for w in self._top_frame.winfo_children(): w.destroy()
        if cursos:
            max_c = cursos[0][1]
            for curso, cnt in cursos:
                row = tk.Frame(self._top_frame, bg=BRANCO)
                row.pack(fill="x", pady=2)
                tk.Label(row, text=curso, font=("Segoe UI", 9),
                         bg=BRANCO, fg=PRETO_TEXTO, width=28,
                         anchor="w").pack(side="left")
                bar_bg = tk.Frame(row, bg=CINZA_CARD, height=14, width=250)
                bar_bg.pack(side="left", padx=6)
                bar_bg.pack_propagate(False)
                tk.Frame(bar_bg, bg=AZUL_MEDIO,
                         width=max(4, int(250 * cnt / max_c)),
                         height=14).place(x=0, y=0)
                tk.Label(row, text=str(cnt), font=FONT_MONO,
                         bg=BRANCO, fg=CINZA_LABEL).pack(side="left")

        # Últimos alunos
        for w in self._rec_frame.winfo_children(): w.destroy()
        ultimos = self.db.alunos.ultimos(5)
        if ultimos:
            for row in ultimos:
                f = tk.Frame(self._rec_frame, bg=BRANCO)
                f.pack(fill="x", pady=2)
                tk.Label(f, text=f"#{row[0]}", font=FONT_MONO,
                         bg=CINZA_CARD, fg=CINZA_LABEL,
                         width=5, padx=4, pady=2).pack(side="left", padx=(0, 8))
                tk.Label(f, text=row[1], font=("Segoe UI", 9, "bold"),
                         bg=BRANCO, fg=PRETO_TEXTO).pack(side="left")
                tk.Label(f, text=row[7], font=("Segoe UI", 8),
                         bg=BRANCO, fg=CINZA_LABEL).pack(side="right")
        else:
            tk.Label(self._rec_frame, text="Nenhum aluno cadastrado.",
                     font=FONT_LABEL, bg=BRANCO, fg=CINZA_LABEL).pack()
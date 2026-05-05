import tkinter as tk
from utils.estilos import (AZUL_ESCURO, AZUL_MEDIO, AZUL_BORDA, AZUL_CLARO,
                            BRANCO, CINZA_LABEL, CINZA_BORDA, VERMELHO,
                            FONT_ENTRY, FONT_LABEL)


class LoginWindow(tk.Tk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.title("Login — Sistema Acadêmico")
        self.geometry("420x520")
        self.configure(bg=AZUL_ESCURO)
        self.resizable(False, False)
        self.usuario_logado = None
        self.role           = None
        self._build()

    def _build(self):
        tk.Label(self, text="🎓", font=("Segoe UI", 48),
                 bg=AZUL_ESCURO, fg=BRANCO).pack(pady=(50, 8))
        tk.Label(self, text="Sistema Acadêmico",
                 font=("Segoe UI", 18, "bold"),
                 bg=AZUL_ESCURO, fg=BRANCO).pack()
        tk.Label(self, text="Registro de Alunos",
                 font=("Segoe UI", 11),
                 bg=AZUL_ESCURO, fg=AZUL_BORDA).pack(pady=(2, 30))

        card = tk.Frame(self, bg=BRANCO)
        card.pack(padx=36, fill="x")

        for lbl, attr, show in [
            ("Usuário", "_e_user", ""),
            ("Senha",   "_e_pass", "•"),
        ]:
            tk.Label(card, text=lbl, font=("Segoe UI", 8, "bold"),
                     bg=BRANCO, fg=CINZA_LABEL).pack(anchor="w", padx=20, pady=(16, 4))
            e = tk.Entry(card, font=FONT_ENTRY, show=show,
                         bd=1, relief="solid",
                         highlightthickness=1,
                         highlightbackground=CINZA_BORDA,
                         highlightcolor=AZUL_MEDIO)
            e.pack(fill="x", padx=20, ipady=6)
            setattr(self, attr, e)

        self._e_pass.bind("<Return>", lambda e: self._login())

        self._lbl_erro = tk.Label(card, text="", font=("Segoe UI", 9),
                                   bg=BRANCO, fg=VERMELHO)
        self._lbl_erro.pack(pady=(8, 0))

        tk.Button(card, text="Entrar", font=("Segoe UI", 10, "bold"),
                  bg=AZUL_ESCURO, fg=BRANCO, activebackground=AZUL_MEDIO,
                  relief="flat", cursor="hand2", pady=10,
                  command=self._login).pack(fill="x", padx=20, pady=(10, 20))

        

    def _login(self):
        u = self._e_user.get().strip()
        p = self._e_pass.get()
        if not u or not p:
            self._lbl_erro.configure(text="Preencha usuário e senha.")
            return
        role = self.db.usuarios.login(u, p)
        if role:
            self.usuario_logado = u
            self.role           = role
            self.destroy()
        else:
            self._lbl_erro.configure(text="Usuário ou senha incorretos.")
            self._e_pass.delete(0, "end")
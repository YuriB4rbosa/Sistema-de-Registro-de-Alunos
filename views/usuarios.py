import tkinter as tk
from tkinter import ttk, messagebox

from utils.estilos import (BRANCO, CINZA_BG, CINZA_CARD, CINZA_BORDA,
                            CINZA_LABEL, CINZA_TEXTO, PRETO_TEXTO,
                            AZUL_ESCURO, AZUL_MEDIO, AZUL_CLARO,
                            VERDE, VERDE_BG, VERMELHO, VERMELHO_BG,
                            FONT_ENTRY, FONT_LABEL, FONT_BTN, FONT_MONO)
from utils.widgets import make_btn, make_scrolled_tree


class UsuariosView(tk.Frame):
    

    def __init__(self, parent, db, usuario_atual):
        super().__init__(parent, bg=CINZA_BG)
        self.db            = db
        self.usuario_atual = usuario_atual
        self._build()

    def _build(self):
        
        topo = tk.Frame(self, bg=CINZA_BG)
        topo.pack(fill="x", pady=(0, 14))
        tk.Label(topo, text="Gerenciamento de Usuários",
                 font=("Segoe UI", 14, "bold"),
                 bg=CINZA_BG, fg=PRETO_TEXTO).pack(side="left")
        tk.Label(topo, text="  (somente admin)",
                 font=("Segoe UI", 9),
                 bg=CINZA_BG, fg=CINZA_LABEL).pack(side="left")

        
        card_criar = tk.Frame(self, bg=BRANCO, bd=1, relief="solid",
                              highlightthickness=1, highlightbackground=CINZA_BORDA)
        card_criar.pack(fill="x", pady=(0, 12))

        hdr = tk.Frame(card_criar, bg=CINZA_CARD)
        hdr.pack(fill="x")
        tk.Frame(hdr, bg=AZUL_MEDIO, width=3).pack(side="left", fill="y")
        tk.Label(hdr, text="➕  Criar novo usuário",
                 font=("Segoe UI", 10, "bold"),
                 bg=CINZA_CARD, fg=PRETO_TEXTO,
                 padx=12, pady=8).pack(side="left")

        body = tk.Frame(card_criar, bg=BRANCO)
        body.pack(fill="x", padx=14, pady=12)

        # Campos
        campos = tk.Frame(body, bg=BRANCO)
        campos.pack(fill="x")

        for i, (lbl, attr, show) in enumerate([
            ("Usuário",  "_e_user",  ""),
            ("Senha",    "_e_senha", "•"),
            ("Confirmar","_e_conf",  "•"),
        ]):
            tk.Label(campos, text=lbl, font=("Segoe UI", 8, "bold"),
                     bg=BRANCO, fg=CINZA_LABEL).grid(
                row=0, column=i, sticky="w", padx=(0, 16), pady=(0, 4))
            e = tk.Entry(campos, font=FONT_ENTRY, show=show, width=18,
                         bd=1, relief="solid", bg=BRANCO,
                         highlightthickness=1, highlightbackground=CINZA_BORDA,
                         highlightcolor=AZUL_MEDIO)
            e.grid(row=1, column=i, sticky="ew", padx=(0, 16), ipady=4)
            setattr(self, attr, e)

        # Role
        tk.Label(campos, text="Perfil", font=("Segoe UI", 8, "bold"),
                 bg=BRANCO, fg=CINZA_LABEL).grid(
            row=0, column=3, sticky="w", pady=(0, 4))
        self._c_role = ttk.Combobox(campos, values=["user", "admin"],
                                     font=FONT_ENTRY, state="readonly", width=10)
        self._c_role.set("user")
        self._c_role.grid(row=1, column=3, sticky="ew", padx=(0, 16), ipady=2)

        self._lbl_status = tk.Label(body, text="", font=("Segoe UI", 8),
                                     bg=BRANCO, fg=VERDE)
        self._lbl_status.pack(anchor="w", pady=(8, 0))

        btn_f = tk.Frame(body, bg=BRANCO)
        btn_f.pack(anchor="w", pady=(6, 0))
        make_btn(btn_f, "➕  Criar usuário", AZUL_ESCURO, BRANCO, self._criar)
        make_btn(btn_f, "✕  Limpar", BRANCO, CINZA_TEXTO,
                 self._limpar, borda=CINZA_BORDA)

        # Card: lista de usuários
        card_lista = tk.Frame(self, bg=BRANCO, bd=1, relief="solid",
                              highlightthickness=1, highlightbackground=CINZA_BORDA)
        card_lista.pack(fill="both", expand=True)

        hdr2 = tk.Frame(card_lista, bg=CINZA_CARD)
        hdr2.pack(fill="x")
        tk.Frame(hdr2, bg=AZUL_MEDIO, width=3).pack(side="left", fill="y")
        tk.Label(hdr2, text="👥  Usuários cadastrados",
                 font=("Segoe UI", 10, "bold"),
                 bg=CINZA_CARD, fg=PRETO_TEXTO,
                 padx=12, pady=8).pack(side="left")

        tree_frame = tk.Frame(card_lista, bg=BRANCO)
        tree_frame.pack(fill="both", expand=True, padx=14, pady=12)

        self._tree = make_scrolled_tree(
            tree_frame,
            columns=("id", "usuario", "perfil"),
            headings_cfg={
                "id":      ("ID",      50),
                "usuario": ("Usuário", 200),
                "perfil":  ("Perfil",  100),
            })
        self._tree.tag_configure("admin", foreground=AZUL_ESCURO)
        self._tree.tag_configure("user",  foreground=CINZA_TEXTO)

        btn_del = make_btn(card_lista, "🗑️  Remover selecionado",
                           VERMELHO_BG, VERMELHO, self._deletar,
                           borda=CINZA_BORDA, pack=False)
        btn_del.pack(anchor="e", padx=14, pady=(0, 12))

    # ── Ações ────────────────────────────────────────────────────
    def _criar(self):
        u     = self._e_user.get().strip()
        s     = self._e_senha.get()
        c     = self._e_conf.get()
        role  = self._c_role.get()

        if not u:
            self._status("Nome de usuário obrigatório.", erro=True); return
        if len(s) < 6:
            self._status("Senha deve ter pelo menos 6 caracteres.", erro=True); return
        if s != c:
            self._status("As senhas não coincidem.", erro=True); return

        ok = self.db.usuarios.criar(u, s, role)
        if ok:
            self._status(f"✓ Usuário '{u}' criado com sucesso!")
            self._limpar()
            self.atualizar()
        else:
            self._status(f"Usuário '{u}' já existe.", erro=True)

    def _deletar(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Clique em um usuário na lista para selecioná-lo.")
            return

        dados   = self._tree.item(sel[0], "values")
        id_user = int(dados[0])
        nome    = dados[1]
        role    = dados[2]

        if nome == self.usuario_atual:
            messagebox.showerror("Erro", "Você não pode remover sua própria conta.")
            return

        if role == "admin":
            admins = [r for r in self.db.usuarios.listar() if r[2] == "admin"]
            if len(admins) <= 1:
                messagebox.showerror("Erro", "O sistema precisa de pelo menos 1 admin.")
                return

        if not messagebox.askyesno("Confirmar", f'Remover usuário "{nome}"?'):
            return

        self.db.usuarios.deletar(id_user)
        self.atualizar()
        self._status(f"Usuário '{nome}' removido.")

    def _limpar(self):
        self._e_user.delete(0, "end")
        self._e_senha.delete(0, "end")
        self._e_conf.delete(0, "end")
        self._c_role.set("user")
        self._lbl_status.configure(text="")

    def _status(self, msg, erro=False):
        self._lbl_status.configure(
            text=msg, fg=VERMELHO if erro else VERDE)

    def atualizar(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        for row in self.db.usuarios.listar():
            tag = "admin" if row[2] == "admin" else "user"
            self._tree.insert("", "end", values=row, tags=(tag,))
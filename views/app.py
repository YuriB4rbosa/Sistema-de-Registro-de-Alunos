import tkinter as tk
from tkinter import messagebox, filedialog

from utils.estilos import (AZUL_ESCURO, AZUL_MEDIO, AZUL_CLARO, BRANCO,
                            CINZA_BG, CINZA_CARD, CINZA_BORDA, CINZA_LABEL,
                            CINZA_TEXTO, PRETO_TEXTO, VERDE, VERDE_BG,
                            VERMELHO, VERMELHO_BG, CORAL, CORAL_BG,
                            AMARELO, AMARELO_BG, ROXO, ROXO_BG,
                            FONT_MONO, FONT_LABEL, aplicar_estilo)
from utils.widgets import make_toast

from services.exportacao import exportar_excel, exportar_csv, fazer_backup

from .dashboard import DashboardView
from .form      import FormView
from .lista     import ListaView
from .historico import HistoricoView
from .usuarios  import UsuariosView

import datetime


class AppWindow(tk.Tk):
    def __init__(self, db, usuario, role):
        super().__init__()
        self.db      = db
        self.usuario = usuario
        self.role    = role

        self.title("Sistema de Registro de Alunos")
        self.geometry("1150x700")
        self.configure(bg=CINZA_BG)
        self.resizable(True, True)
        self.minsize(950, 600)
        self.protocol("WM_DELETE_WINDOW", self._ao_fechar)

        aplicar_estilo(self)
        self._build_header()
        self._build_layout()
        self._build_sidebar()
        self._build_views()
        self._bind_shortcuts()
        self.show_view("dashboard")


    def _ao_fechar(self):
        if messagebox.askokcancel("Sair", "Deseja realmente sair do sistema?"):
            self.destroy()

    def _sair(self):
        self.destroy()

    # ── Header ──────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=AZUL_ESCURO, height=52)
        hdr.pack(fill="x"); hdr.pack_propagate(False)

        tk.Label(hdr, text="🎓", font=("Segoe UI", 18),
                 bg=AZUL_ESCURO, fg=BRANCO).pack(side="left", padx=(16,8), pady=8)
        tk.Label(hdr, text="Sistema Acadêmico",
                 font=("Segoe UI", 13, "bold"),
                 bg=AZUL_ESCURO, fg=BRANCO).pack(side="left")
        tk.Label(hdr, text=" — Registro de Alunos",
                 font=("Segoe UI", 10),
                 bg=AZUL_ESCURO, fg="#85B7EB").pack(side="left")

        tk.Button(hdr, text="Sair", font=("Segoe UI", 8, "bold"),
                  bg=VERMELHO_BG, fg=VERMELHO, relief="flat",
                  cursor="hand2", padx=8, pady=4,
                  command=self._sair).pack(side="right", padx=(6,16), pady=14)

        tk.Label(hdr, text=f"👤 {self.usuario}  ({self.role})",
                 font=FONT_MONO, bg="#0C447C", fg="#B5D4F4",
                 padx=10, pady=4).pack(side="right", padx=6, pady=10)

        self._lbl_count = tk.Label(hdr, text="0 alunos",
                                    font=FONT_MONO, bg="#0C447C",
                                    fg="#B5D4F4", padx=12, pady=4)
        self._lbl_count.pack(side="right", padx=6, pady=10)

    # ── Layout ──────────────────────────────────────────────────
    def _build_layout(self):
        self._main = tk.Frame(self, bg=CINZA_BG)
        self._main.pack(fill="both", expand=True)

        self._sidebar = tk.Frame(self._main, bg=BRANCO, width=215)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)

        tk.Frame(self._main, bg=CINZA_BORDA, width=1).pack(side="left", fill="y")

        self._content = tk.Frame(self._main, bg=CINZA_BG)
        self._content.pack(side="left", fill="both", expand=True)

    # ── Sidebar ─────────────────────────────────────────────────
    def _build_sidebar(self):
        f = self._sidebar
        tk.Label(f, text="MENU", font=("Segoe UI", 8, "bold"),
                 bg=BRANCO, fg=CINZA_LABEL).pack(anchor="w", padx=16, pady=(16,4))

        self._nav_btns = {}
        nav_items = [("dashboard","📊  Dashboard"),
                     ("form",     "✏️  Cadastrar"),
                     ("list",     "📋  Alunos"),
                     ("history",  "🕓  Histórico")]
        if self.role == "admin":
            nav_items.append(("users", "👥  Usuários"))

        for key, label in nav_items:
            btn = tk.Button(f, text=label, font=FONT_LABEL,
                            bg=BRANCO, fg=CINZA_TEXTO,
                            activebackground=AZUL_CLARO,
                            activeforeground=AZUL_ESCURO,
                            relief="flat", anchor="w", padx=16, pady=8,
                            cursor="hand2",
                            command=lambda k=key: self.show_view(k))
            btn.pack(fill="x", padx=8, pady=1)
            self._nav_btns[key] = btn

        tk.Frame(f, bg=CINZA_BORDA, height=1).pack(fill="x", padx=12, pady=8)
        tk.Label(f, text="FERRAMENTAS", font=("Segoe UI", 8, "bold"),
                 bg=BRANCO, fg=CINZA_LABEL).pack(anchor="w", padx=16, pady=(4,4))

        for label, cmd in [
            ("📥  Importar CSV",      self._importar_csv),
            ("📥  Importar Excel",    self._importar_excel),
            ("📤  Exportar Excel",    self._exportar_excel),
            ("📤  Exportar CSV",      self._exportar_csv),
            ("🖨️  Relatório PDF",     self._relatorio_pdf),
            ("💾  Fazer backup",      self._fazer_backup),
            ("🗑️  Limpar formulário", self._limpar_form),
        ]:
            tk.Button(f, text=label, font=FONT_LABEL, bg=BRANCO, fg=CINZA_TEXTO,
                      activebackground=CINZA_CARD, relief="flat", anchor="w",
                      padx=16, pady=7, cursor="hand2",
                      command=cmd).pack(fill="x", padx=8, pady=1)

        tk.Frame(f, bg=CINZA_BORDA, height=1).pack(fill="x", padx=12, pady=8)
        self._btn_tema = tk.Button(f, text="🌙  Tema escuro",
                                    font=FONT_LABEL, bg=BRANCO, fg=CINZA_TEXTO,
                                    activebackground=CINZA_CARD,
                                    relief="flat", anchor="w", padx=16, pady=7,
                                    cursor="hand2",
                                    command=self._alternar_tema)
        self._btn_tema.pack(fill="x", padx=8, pady=1)
    def _build_views(self):
        self._view_dashboard = DashboardView(self._content, self.db)
        self._view_form      = FormView(
            self._content, self.db, self.usuario,
            on_save=self._on_form_save)
        self._view_list      = ListaView(
            self._content, self.db, self.usuario,
            on_editar=self._editar_aluno,
            on_toast=self._toast_kind)
        self._view_history   = HistoricoView(self._content, self.db)
        self._view_users     = UsuariosView(self._content, self.db, self.usuario)

        self._views = {
            "dashboard": self._view_dashboard,
            "form":      self._view_form,
            "list":      self._view_list,
            "history":   self._view_history,
            "users":     self._view_users,
        }

    def show_view(self, key):
        # Bloqueia acesso à tela de usuários para não-admins
        if key == "users" and self.role != "admin":
            return
        for frame in self._views.values(): frame.pack_forget()
        self._views[key].pack(fill="both", expand=True, padx=20, pady=16)

        for k, btn in self._nav_btns.items():
            if k == key:
                btn.configure(bg=AZUL_CLARO, fg=AZUL_ESCURO,
                               font=("Segoe UI", 9, "bold"))
            else:
                btn.configure(bg=BRANCO, fg=CINZA_TEXTO, font=FONT_LABEL)

        if key == "dashboard": self._view_dashboard.atualizar(); self._atualizar_count()
        if key == "list":      self._view_list.atualizar();      self._atualizar_count()
        if key == "history":   self._view_history.atualizar()
        if key == "users":     self._view_users.atualizar()

    # ── Callbacks ───────────────────────────────────────────────
    def _on_form_save(self, msg, kind="verde"):
        self._atualizar_count()
        self._toast_kind(msg, kind)

    def _editar_aluno(self, id_aluno):
        self._view_form.carregar_aluno(id_aluno)
        self.show_view("form")

    def _limpar_form(self):
        self._view_form.limpar()
        self.show_view("form")

    def _toast_kind(self, msg, kind="verde"):
        paletas = {
            "verde": (VERDE_BG,  VERDE),
            "azul":  (AZUL_CLARO, AZUL_ESCURO),
            "coral": (CORAL_BG,  CORAL),
            "roxo":  (ROXO_BG,   ROXO),
            "amarelo": (AMARELO_BG, AMARELO),
        }
        bg, fg = paletas.get(kind, (VERDE_BG, VERDE))
        make_toast(self, msg, bg, fg)

    def _atualizar_count(self):
        n = self.db.alunos.contar()
        self._lbl_count.configure(
            text=f"{n} {'aluno' if n == 1 else 'alunos'}")

    # ── Ferramentas ─────────────────────────────────────────────
    def _importar_csv(self):
        from services.exportacao import importar_csv
        path = filedialog.askopenfilename(
            title="Importar CSV",
            filetypes=[("CSV", "*.csv")])
        if not path: return
        self._processar_importacao(importar_csv(path))

    def _importar_excel(self):
        from services.exportacao import importar_excel
        path = filedialog.askopenfilename(
            title="Importar Excel",
            filetypes=[("Excel", "*.xlsx *.xls")])
        if not path: return
        self._processar_importacao(importar_excel(path))

    def _processar_importacao(self, resultado):
        registros, erros = resultado
        if not registros and erros:
            messagebox.showerror("Erro na importação", "\n".join(erros)); return

        msg = f"Encontrados {len(registros)} registros para importar."
        if erros:
            msg += f"\n\n⚠️ {len(erros)} linha(s) ignorada(s):\n" + "\n".join(erros[:5])
            if len(erros) > 5:
                msg += f"\n... e mais {len(erros)-5} erro(s)."

        if not messagebox.askyesno("Confirmar importação", msg + "\n\nDeseja continuar?"):
            return

        importados = 0
        falhas     = []
        for dados in registros:
            try:
                self.db.alunos.registrar(dados)
                self.db.historico.registrar(
                    self.usuario, "CADASTRO",
                    detalhes=f"Importado de arquivo | {datetime.date.today().strftime('%d/%m/%Y')}")
                importados += 1
            except Exception as e:
                falhas.append(str(e))

        self._atualizar_count()
        msg_final = f"✅  {importados} aluno(s) importado(s) com sucesso!"
        if falhas:
            msg_final += f"\n⚠️ {len(falhas)} erro(s) durante o cadastro."
        self._toast_kind(f"📥  {importados} aluno(s) importado(s)!", "verde")
        if falhas:
            messagebox.showwarning("Importação concluída com avisos", msg_final)
    def _relatorio_pdf(self):
        from services.pdf import gerar_relatorio_pdf
        dados = self.db.alunos.listar()
        if not dados:
            messagebox.showwarning("Aviso", "Nenhum aluno para gerar relatório.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF", "*.pdf")],
            initialfile=f"relatorio_alunos_{datetime.date.today().strftime('%d-%m-%Y')}.pdf")
        if not path: return
        gerar_relatorio_pdf(dados, path,
                             titulo="Relatório Geral de Alunos",
                             filtros_desc=f"Todos os alunos — {datetime.date.today().strftime('%d/%m/%Y')}")
        self.db.historico.registrar(self.usuario, "RELATÓRIO PDF",
                                     detalhes=f"{len(dados)} alunos")
        self._toast_kind("🖨️  Relatório gerado!", "roxo")

    def _alternar_tema(self):
        from utils.estilos import alternar_tema, aplicar_estilo
        tema = alternar_tema()
        aplicar_estilo(self)
        # Atualiza ícone do botão
        if tema == "escuro":
            self._btn_tema.configure(text="☀️  Tema claro")
        else:
            self._btn_tema.configure(text="🌙  Tema escuro")
        # Força recarregamento da view atual
        for key, frame in self._views.items():
            if frame.winfo_ismapped():
                self.show_view(key)
                break

    def _exportar_excel(self):
        
        try:
            import openpyxl
        except ImportError:
            messagebox.showerror("Erro", "Instale openpyxl:\n  pip install openpyxl")
            return
        
        dados = self.db.alunos.listar()
        if not dados:
            messagebox.showwarning("Aviso", "Nenhum aluno para exportar.")
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", 
            filetypes=[("Excel", "*.xlsx")],
            initialfile=f"alunos_{datetime.date.today().strftime('%d-%m-%Y')}.xlsx"
        )
        if not path:
            return
        
        exportar_excel(dados, path)
        self._toast_kind("📤  Excel exportado!", "verde")

    def _exportar_csv(self):
        dados = self.db.alunos.listar()
        if not dados:
            messagebox.showwarning("Aviso", "Nenhum aluno para exportar."); return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV","*.csv")],
            initialfile=f"alunos_{datetime.date.today().strftime('%d-%m-%Y')}.csv")
        if not path: return
        exportar_csv(dados, path)
        self._toast_kind("📤  CSV exportado!", "verde")

    def _fazer_backup(self):
        try:
            fazer_backup()
            self._toast_kind("💾  Backup salvo em /backups/", "amarelo")
        except FileNotFoundError as e:
            messagebox.showerror("Erro", str(e))

    # ── Atalhos de teclado ───────────────────────────────────────
    def _bind_shortcuts(self):
        self.bind("<Control-n>", lambda e: (self._limpar_form(), self.show_view("form")))
        self.bind("<Control-l>", lambda e: self.show_view("list"))
        self.bind("<Control-d>", lambda e: self.show_view("dashboard"))
        self.bind("<Control-h>", lambda e: self.show_view("history"))
        self.bind("<Control-u>", lambda e: self.show_view("users") if self.role == "admin" else None)
        self.bind("<Control-s>", lambda e: self._view_form.salvar() if self._view_form.winfo_ismapped() else None)
        self.bind("<Control-f>", lambda e: self._focar_busca())
        self.bind("<Escape>",    lambda e: self._view_form.limpar())

    def _focar_busca(self):
        self.show_view("list")
        
        try:
            self._view_list._e_busca.focus_set()
            self._view_list._e_busca.select_range(0, "end")
        except Exception:
            pass

    # ── Fechar / Sair ────────────────────────────────────────────
    
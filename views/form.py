import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import datetime

from utils.estilos import (BRANCO, CINZA_BG, CINZA_CARD, CINZA_BORDA,
                            CINZA_LABEL, PRETO_TEXTO, AZUL_ESCURO,
                            AZUL_MEDIO, AZUL_CLARO, AZUL_BORDA,
                            VERDE, VERDE_BG, VERMELHO, ROXO, ROXO_BG,
                            FONT_ENTRY, FONT_BTN, FONT_LABEL)
from utils.widgets import make_btn, make_card, make_field
from services.validacao import validar_aluno, mascarar_telefone
from services.foto import salvar_foto, carregar_foto_tk
from services.pdf  import gerar_ficha_pdf

CURSOS = [
    "ADS","Ciência da Computação","Engenharia de Software","Sistemas de Informação",
    "Ciência de Dados","Cibersegurança","Inteligência Artificial","Redes de Computadores",
    "Gestão de TI","Matemática","Física","Estatística","Jogos Digitais","Banco de Dados",
    "Medicina","Psicologia","Enfermagem","Nutrição","Fisioterapia","Odontologia",
    "Farmácia","Biomedicina","Educação Física","Veterinária","Fonoaudiologia",
    "Biologia","Biotecnologia","Radiologia","Engenharia Civil","Engenharia Mecânica",
    "Engenharia Elétrica","Engenharia de Produção","Engenharia Química",
    "Engenharia de Computação","Engenharia Ambiental","Engenharia Mecatrônica",
    "Engenharia Biomédica","Direito","Administração","Ciências Contábeis","Economia",
    "Relações Internacionais","Marketing","Recursos Humanos","Logística",
    "Comércio Exterior","Pedagogia","História","Geografia","Filosofia","Sociologia",
    "Serviço Social","Design Gráfico","Design de Interiores","Publicidade e Propaganda",
    "Jornalismo","Relações Públicas","Cinema e Audiovisual","Artes Visuais","Moda",
    "Arquitetura e Urbanismo","Letras (Português/Inglês)","Gastronomia","Eventos",
]


class FormView(tk.Frame):
    

    def __init__(self, parent, db, usuario, on_save=None):
        super().__init__(parent, bg=CINZA_BG)
        self.db         = db
        self.usuario    = usuario
        self.on_save    = on_save       
        self._foto_path = ""
        self._photo_ref = None
        self._editando  = None          
        self._build()

    
    
    
    
    
    # ── Construção da UI ─────────────────────────────────────────
    def _build(self):
        # Busca por ID
        id_card = tk.Frame(self, bg=BRANCO, bd=1, relief="solid",
                           highlightthickness=1, highlightbackground=CINZA_BORDA)
        id_card.pack(fill="x", pady=(0, 10))
        id_inner = tk.Frame(id_card, bg=BRANCO)
        id_inner.pack(fill="x", padx=14, pady=10)
        tk.Label(id_inner, text="🔍  Buscar aluno por ID",
                 font=("Segoe UI", 8, "bold"), bg=BRANCO,
                 fg=CINZA_LABEL).pack(side="left", padx=(0, 10))
        self._e_id = tk.Entry(id_inner, font=FONT_ENTRY, width=8,
                               bd=1, relief="solid", bg=BRANCO,
                               fg=PRETO_TEXTO, justify="center",
                               highlightthickness=1,
                               highlightbackground=CINZA_BORDA,
                               highlightcolor=AZUL_MEDIO)
        self._e_id.pack(side="left", ipady=3, padx=(0, 6))
        self._e_id.bind("<Return>", lambda e: self.buscar_por_id())
        make_btn(id_inner, "Carregar", AZUL_MEDIO, BRANCO, self.buscar_por_id)
        self._lbl_id_status = tk.Label(id_inner, text="",
                                        font=("Segoe UI", 8),
                                        bg=BRANCO, fg=CINZA_LABEL)
        self._lbl_id_status.pack(side="left", padx=10)

        # Banner de edição
        self._banner = tk.Frame(self, bg=AZUL_CLARO, bd=1, relief="solid",
                                highlightthickness=1, highlightbackground=AZUL_BORDA)
        self._banner_lbl = tk.Label(self._banner, text="", font=FONT_LABEL,
                                    bg=AZUL_CLARO, fg=AZUL_ESCURO)
        self._banner_lbl.pack(side="left", padx=12, pady=6)
        tk.Button(self._banner, text="✕ Cancelar", font=("Segoe UI", 8),
                  bg=AZUL_CLARO, fg=AZUL_MEDIO, relief="flat", cursor="hand2",
                  command=self.limpar).pack(side="right", padx=12)

        # Card dados pessoais
        body1 = make_card(self, "Dados pessoais", "👤")
        foto_frame = tk.Frame(body1, bg=BRANCO)
        foto_frame.grid(row=0, column=0, rowspan=6, padx=(0, 16), sticky="n")
        self._foto_btn = tk.Button(foto_frame,
                                   text="📷\n\nClique para\nadicionar foto",
                                   font=("Segoe UI", 8), width=14, height=7,
                                   bg=CINZA_CARD, fg=CINZA_LABEL,
                                   relief="solid", bd=1, cursor="hand2",
                                   activebackground=AZUL_CLARO,
                                   command=self._escolher_foto)
        self._foto_btn.pack()
        for i in range(1, 4): body1.columnconfigure(i, weight=1)
        self._e_nome  = make_field(body1, "Nome completo", 0, 1, colspan=2, width=35)
        self._e_data  = self._build_date(body1, 0, 3)
        self._e_email = make_field(body1, "Email",    1, 1, colspan=2, width=35)
        self._e_tel   = make_field(body1, "Telefone", 1, 3, width=18)
        self._e_tel.bind("<KeyRelease>", self._on_tel)

        # Card acadêmico
        body2 = make_card(self, "Informações acadêmicas e endereço", "🏫")
        for i, w in enumerate([1, 2, 2]): body2.columnconfigure(i, weight=w)
        tk.Label(body2, text="Sexo *", font=("Segoe UI", 8, "bold"),
                 bg=BRANCO, fg=CINZA_LABEL).grid(row=0, column=0, sticky="w", pady=(6,2))
        self._c_sexo = ttk.Combobox(body2, values=["M","F","Outro"],
                                     font=FONT_ENTRY, state="readonly", width=12)
        self._c_sexo.grid(row=1, column=0, sticky="ew", padx=(0,8))
        tk.Label(body2, text="Curso *", font=("Segoe UI", 8, "bold"),
                 bg=BRANCO, fg=CINZA_LABEL).grid(row=0, column=1, sticky="w", pady=(6,2))
        self._c_curso = ttk.Combobox(body2, values=CURSOS,
                                      font=FONT_ENTRY, state="readonly", width=28)
        self._c_curso.grid(row=1, column=1, sticky="ew", padx=(0,8))
        self._e_end = make_field(body2, "Endereço completo", 1, 0, colspan=3, width=60)

        # Card observações
        body3 = make_card(self, "Observações", "📝")
        tk.Label(body3, text="Anotações livres (opcional)",
                 font=("Segoe UI", 8, "bold"), bg=BRANCO,
                 fg=CINZA_LABEL).pack(anchor="w", pady=(0, 4))
        self._t_obs = tk.Text(body3, font=FONT_ENTRY, height=3,
                               bd=1, relief="solid", bg=BRANCO,
                               fg=PRETO_TEXTO, wrap="word",
                               highlightthickness=1,
                               highlightbackground=CINZA_BORDA,
                               highlightcolor=AZUL_MEDIO)
        self._t_obs.pack(fill="x")

        # Botões
        btn_f = tk.Frame(self, bg=CINZA_BG)
        btn_f.pack(fill="x", pady=(4, 0))
        self._btn_salvar    = make_btn(btn_f, "💾  Cadastrar aluno",
                                       AZUL_ESCURO, BRANCO, self.salvar)
        self._btn_atualizar = make_btn(btn_f, "🔄  Salvar alterações",
                                       VERDE, BRANCO, self.atualizar, pack=False)
        self._btn_atualizar.pack(side="left", padx=(0,6))
        self._btn_atualizar.pack_forget()
        make_btn(btn_f, "🖨️  Gerar PDF", ROXO_BG, ROXO, self.gerar_pdf, borda=CINZA_BORDA)
        make_btn(btn_f, "✕  Limpar",    BRANCO, CINZA_LABEL, self.limpar, borda=CINZA_BORDA)

    def _build_date(self, parent, row, col):
        tk.Label(parent, text="Data de nascimento *",
                 font=("Segoe UI", 8, "bold"), bg=BRANCO,
                 fg=CINZA_LABEL).grid(row=row*2, column=col, sticky="w", pady=(6,2))
        d = DateEntry(parent, font=FONT_ENTRY, width=16,
                      background=AZUL_ESCURO, foreground=BRANCO,
                      borderwidth=1, year=2005, date_pattern="dd/mm/yyyy",
                      maxdate=datetime.date.today())
        d.grid(row=row*2+1, column=col, sticky="ew", padx=(0,8))
        return d

    # ── Ações ────────────────────────────────────────────────────
    def _form_dados(self):
        return [self._e_nome.get().strip(), self._e_email.get().strip(),
                self._e_tel.get().strip(),  self._c_sexo.get(),
                self._e_data.get(),         self._e_end.get().strip(),
                self._c_curso.get(),        self._foto_path,
                self._t_obs.get("1.0", "end").strip()]

    def salvar(self):
        dados = self._form_dados()
        erros = validar_aluno(dados)
        if erros:
            messagebox.showerror("Campos inválidos", "\n".join(erros)); return
        rowid = self.db.alunos.registrar(dados)
        self.db.historico.registrar(self.usuario, "CADASTRO", rowid, dados[0],
                                     f"Curso: {dados[6]} | "
                                     f"{datetime.date.today().strftime('%d/%m/%Y')}")
        self.limpar()
        if self.on_save: self.on_save("✅  Aluno cadastrado com sucesso!")

    def atualizar(self):
        if self._editando is None: return
        dados = self._form_dados()
        erros = validar_aluno(dados)
        if erros:
            messagebox.showerror("Campos inválidos", "\n".join(erros)); return
        self.db.alunos.atualizar(self._editando, dados)
        self.db.historico.registrar(self.usuario, "ATUALIZAÇÃO",
                                     self._editando, dados[0],
                                     f"Curso: {dados[6]}")
        self.limpar()
        if self.on_save: self.on_save("🔄  Aluno atualizado!")

    def gerar_pdf(self):
        if self._editando is None:
            messagebox.showwarning("Aviso",
                "Carregue um aluno primeiro para gerar o PDF."); return
        dados = self.db.alunos.buscar_por_id(self._editando)
        if not dados: return
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF","*.pdf")],
            initialfile=f"ficha_{dados[1].split()[0].lower()}_{dados[0]}.pdf")
        if not path: return
        gerar_ficha_pdf(dados, path)
        self.db.historico.registrar(self.usuario, "PDF", dados[0], dados[1])
        if self.on_save: self.on_save("🖨️  PDF gerado!", kind="roxo")

    def limpar(self):
        self._editando = None; self._foto_path = ""
        for e in (self._e_nome, self._e_email, self._e_tel, self._e_end):
            e.delete(0, "end")
        self._c_sexo.set(""); self._c_curso.set("")
        self._t_obs.delete("1.0", "end")
        self._lbl_id_status.configure(text="")
        self._foto_btn.configure(image="", text="📷\n\nClique para\nadicionar foto",
                                  compound="center", width=14, height=7)
        self._banner.pack_forget()
        self._btn_salvar.pack(side="left", padx=(0,6))
        self._btn_atualizar.pack_forget()

    def carregar_aluno(self, id_aluno):
        dados = self.db.alunos.buscar_por_id(id_aluno)
        if not dados:
            messagebox.showerror("Erro", "Aluno não encontrado."); return
        self._editando = id_aluno
        self._e_nome.delete(0,"end");  self._e_nome.insert(0, dados[1])
        self._e_email.delete(0,"end"); self._e_email.insert(0, dados[2])
        self._e_tel.delete(0,"end");   self._e_tel.insert(0, dados[3])
        self._c_sexo.set(dados[4])
        try: self._e_data.set_date(dados[5])
        except Exception: pass
        self._e_end.delete(0,"end"); self._e_end.insert(0, dados[6])
        self._c_curso.set(dados[7])
        self._foto_path = dados[8] or ""
        self._t_obs.delete("1.0", "end")
        if dados[9]: self._t_obs.insert("1.0", dados[9])
        if self._foto_path:
            try:
                self._photo_ref = carregar_foto_tk(self._foto_path)
                self._foto_btn.configure(image=self._photo_ref, text="",
                                          width=110, height=110, compound="center")
            except Exception:
                pass
        self._banner_lbl.configure(text=f"✏️  Editando: #{id_aluno} — {dados[1]}")
        self._banner.pack(fill="x", pady=(0, 10))
        self._btn_salvar.pack_forget()
        self._btn_atualizar.pack(side="left", padx=(0,6))

    def buscar_por_id(self):
        raw = self._e_id.get().strip()
        if not raw:
            self._lbl_id_status.configure(text="Digite um ID.", fg=CINZA_LABEL); return
        try:    id_aluno = int(raw)
        except: self._lbl_id_status.configure(text="ID inválido.", fg=VERMELHO); return
        if not self.db.alunos.buscar_por_id(id_aluno):
            self._lbl_id_status.configure(
                text=f"ID #{id_aluno} não encontrado.", fg=VERMELHO); return
        self._lbl_id_status.configure(text=f"✓ #{id_aluno} carregado.", fg=VERDE)
        self.carregar_aluno(id_aluno)
        self._e_id.delete(0, "end")

    # ── Foto ─────────────────────────────────────────────────────
    def _escolher_foto(self):
        path = filedialog.askopenfilename(
            title="Selecionar foto",
            filetypes=[("Imagens","*.jpg *.jpeg *.png *.bmp *.webp")])
        if not path: return
        self._foto_path = salvar_foto(path)
        try:
            self._photo_ref = carregar_foto_tk(self._foto_path)
            self._foto_btn.configure(image=self._photo_ref, text="",
                                      width=110, height=110, compound="center")
        except Exception as e:
            messagebox.showwarning("Foto", str(e))

    def _on_tel(self, event=None):
        fmt = mascarar_telefone(self._e_tel.get())
        self._e_tel.delete(0, "end"); self._e_tel.insert(0, fmt)


# imports extras necessários para o módulo
import os
from utils.estilos import VERDE
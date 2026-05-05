import tkinter as tk
from tkinter import ttk, messagebox

from utils.estilos import (BRANCO, CINZA_BG, CINZA_CARD, CINZA_BORDA,
                            CINZA_LABEL, PRETO_TEXTO, AZUL_ESCURO, AZUL_MEDIO,
                            AZUL_CLARO, VERDE, VERDE_BG, VERMELHO, VERMELHO_BG,
                            CORAL, CORAL_BG, FONT_ENTRY, FONT_MONO, FONT_LABEL)
from utils.widgets import make_btn, make_scrolled_tree

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

PAGE_SIZE = 50
_PLACEHOLDER = "Buscar por ID, nome, email, curso..."


class ListaView(tk.Frame):
    

    def __init__(self, parent, db, usuario,
                 on_editar=None, on_toast=None):
        super().__init__(parent, bg=CINZA_BG)
        self.db         = db
        self.usuario    = usuario
        self.on_editar  = on_editar     
        self.on_toast   = on_toast      
        self._dados     = []
        self._pagina    = 0
        self._build()

    
    
    
    
    def _build(self):
        # Barra de busca
        bar = tk.Frame(self, bg=CINZA_BG)
        bar.pack(fill="x", pady=(0, 6))
        tk.Label(bar, text="🔍", font=("Segoe UI",11), bg=CINZA_BG).pack(side="left")
        self._e_busca = tk.Entry(bar, font=FONT_ENTRY, width=28,
                                  bd=1, relief="solid", bg=BRANCO, fg=CINZA_LABEL,
                                  highlightthickness=1, highlightbackground=CINZA_BORDA,
                                  highlightcolor=AZUL_MEDIO)
        self._e_busca.pack(side="left", padx=6, ipady=4)
        self._e_busca.insert(0, _PLACEHOLDER)
        self._e_busca.bind("<FocusIn>",    self._focus_in)
        self._e_busca.bind("<FocusOut>",   self._focus_out)
        self._e_busca.bind("<KeyRelease>", lambda e: self.filtrar())
        make_btn(bar, "Buscar", AZUL_MEDIO, BRANCO, self.filtrar)
        make_btn(bar, "🗑️  Deletar", VERMELHO_BG, VERMELHO,
                 self._deletar, borda=CINZA_BORDA, side="right", padx=(6,0))

        
        
        
        # Filtros combinados
        f_frame = tk.Frame(self, bg=CINZA_CARD, bd=1, relief="solid",
                           highlightthickness=1, highlightbackground=CINZA_BORDA)
        f_frame.pack(fill="x", pady=(0,8))
        fi = tk.Frame(f_frame, bg=CINZA_CARD)
        fi.pack(fill="x", padx=12, pady=8)

        tk.Label(fi, text="Filtros:", font=("Segoe UI",8,"bold"),
                 bg=CINZA_CARD, fg=CINZA_LABEL).pack(side="left", padx=(0,10))

        for lbl, attr, vals, w in [
            ("Curso:",  "_f_curso", ["(Todos)"]+CURSOS, 20),
            ("Sexo:",   "_f_sexo",  ["(Todos)","M","F","Outro"], 8),
        ]:
            tk.Label(fi, text=lbl, font=("Segoe UI",8),
                     bg=CINZA_CARD, fg=CINZA_LABEL).pack(side="left")
            cb = ttk.Combobox(fi, values=vals, font=("Segoe UI",8),
                               width=w, state="readonly")
            cb.set(vals[0]); cb.pack(side="left", padx=(4,12))
            setattr(self, attr, cb)

        for lbl, attr in [("Idade mín:", "_f_imin"), ("máx:", "_f_imax")]:
            tk.Label(fi, text=lbl, font=("Segoe UI",8),
                     bg=CINZA_CARD, fg=CINZA_LABEL).pack(side="left")
            e = tk.Entry(fi, font=("Segoe UI",8), width=4, bd=1, relief="solid")
            e.pack(side="left", padx=(4,8), ipady=2)
            setattr(self, attr, e)

        make_btn(fi, "Aplicar", AZUL_MEDIO, BRANCO, self.filtrar)
        make_btn(fi, "Limpar filtros", BRANCO, CINZA_LABEL,
                 self._limpar_filtros, borda=CINZA_BORDA)

       
       
       
        # Tabela
        card = tk.Frame(self, bg=BRANCO, bd=1, relief="solid",
                        highlightthickness=1, highlightbackground=CINZA_BORDA)
        card.pack(fill="both", expand=True)
        self._tree = make_scrolled_tree(card,
            columns=("id","nome","email","telefone","sexo","nascimento","curso"),
            headings_cfg={
                "id":         ("ID",        45),
                "nome":       ("Nome",      170),
                "email":      ("Email",     170),
                "telefone":   ("Telefone",  105),
                "sexo":       ("Sexo",       60),
                "nascimento": ("Nasc.",      90),
                "curso":      ("Curso",     150),
            })
        self._tree.bind("<Double-1>", self._on_double)

       
       
       
        # Paginação
        pag = tk.Frame(self, bg=CINZA_BG)
        pag.pack(fill="x", pady=(6,0))
        self._btn_prev = make_btn(pag, "← Anterior", BRANCO, CINZA_LABEL,
                                   self._pag_prev, borda=CINZA_BORDA)
        self._lbl_pag  = tk.Label(pag, text="", font=FONT_MONO,
                                   bg=CINZA_BG, fg=CINZA_LABEL)
        self._lbl_pag.pack(side="left", padx=12)
        self._btn_next = make_btn(pag, "Próximo →", BRANCO, CINZA_LABEL,
                                   self._pag_next, borda=CINZA_BORDA)
        self._lbl_res  = tk.Label(pag, text="", font=("Segoe UI",8),
                                   bg=CINZA_BG, fg=CINZA_LABEL)
        self._lbl_res.pack(side="right")

    
    
    
    
    # ── Dados ────────────────────────────────────────────────────
    def atualizar(self, dados=None):
        if dados is None: dados = self.db.alunos.listar()
        self._dados = dados; self._pagina = 0
        self._renderizar()

    def filtrar(self):
        q = self._e_busca.get().strip()
        if q == _PLACEHOLDER: q = ""
        curso = self._f_curso.get(); curso = "" if curso == "(Todos)" else curso
        sexo  = self._f_sexo.get();  sexo  = "" if sexo  == "(Todos)" else sexo
        try:    imin = int(self._f_imin.get()) if self._f_imin.get() else None
        except: imin = None
        try:    imax = int(self._f_imax.get()) if self._f_imax.get() else None
        except: imax = None

        dados = self.db.alunos.buscar_com_filtros(q, curso, sexo, imin, imax)
        if q.isdigit():
            exato = [r for r in dados if str(r[0]) == q]
            resto  = [r for r in dados if str(r[0]) != q]
            dados  = exato + resto
        self.atualizar(dados)

    def _renderizar(self):
        for item in self._tree.get_children(): self._tree.delete(item)
        total  = len(self._dados)
        inicio = self._pagina * PAGE_SIZE
        fim    = min(inicio + PAGE_SIZE, total)
        for i, row in enumerate(self._dados[inicio:fim]):
            tag = "par" if i % 2 == 0 else "impar"
            self._tree.insert("","end",
                               values=(row[0],row[1],row[2],row[3],
                                       row[4],row[5],row[7]),
                               tags=(tag,))
        total_pags = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
        self._lbl_pag.configure(text=f"Pág. {self._pagina+1} / {total_pags}")
        self._lbl_res.configure(
            text=f"Exibindo {inicio+1}–{fim} de {total}" if total else "Nenhum resultado")
        self._btn_prev.configure(state="normal" if self._pagina > 0  else "disabled")
        self._btn_next.configure(state="normal" if fim < total        else "disabled")

    def _pag_prev(self):
        if self._pagina > 0: self._pagina -= 1; self._renderizar()

    def _pag_next(self):
        if (self._pagina+1)*PAGE_SIZE < len(self._dados):
            self._pagina += 1; self._renderizar()

    def _on_double(self, event):
        sel = self._tree.selection()
        if not sel: return
        id_aluno = int(self._tree.item(sel[0], "values")[0])
        if self.on_editar: self.on_editar(id_aluno)

    def _deletar(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um aluno na tabela."); return
        dados    = self._tree.item(sel[0], "values")
        id_aluno = int(dados[0]); nome = dados[1]
        if not messagebox.askyesno("Confirmar",
                                   f'Deletar "{nome}"? Não pode ser desfeito.'): return
        self.db.alunos.deletar(id_aluno)
        self.db.historico.registrar(self.usuario, "EXCLUSÃO", id_aluno, nome)
        self.atualizar()
        if self.on_toast: self.on_toast(f'🗑️  "{nome}" removido.', "coral")

    def _limpar_filtros(self):
        self._f_curso.set("(Todos)"); self._f_sexo.set("(Todos)")
        self._f_imin.delete(0,"end"); self._f_imax.delete(0,"end")
        self._e_busca.delete(0,"end"); self._e_busca.insert(0, _PLACEHOLDER)
        self._e_busca.configure(fg=CINZA_LABEL)
        self.atualizar()

    def _focus_in(self, e):
        if self._e_busca.get() == _PLACEHOLDER:
            self._e_busca.delete(0,"end"); self._e_busca.configure(fg=PRETO_TEXTO)

    def _focus_out(self, e):
        if not self._e_busca.get():
            self._e_busca.insert(0, _PLACEHOLDER)
            self._e_busca.configure(fg=CINZA_LABEL)
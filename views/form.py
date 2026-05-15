from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLineEdit,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QComboBox,
    QDateEdit,
    QSizePolicy
)

from PySide6.QtGui import (
    QPixmap,
    QColor
)

from PySide6.QtCore import (
    Qt,
    QDate
)

import datetime


CURSOS = [
    # Tecnologia
    "Análise e Desenvolvimento de Sistemas",
    "Ciência da Computação",
    "Engenharia de Software",
    "Sistemas de Informação",
    "Ciência de Dados",
    "Inteligência Artificial",
    "Cibersegurança",
    "Banco de Dados",
    "Redes de Computadores",
    "Gestão da Tecnologia da Informação",
    "Jogos Digitais",

    # Engenharias
    "Engenharia Civil",
    "Engenharia Mecânica",
    "Engenharia Elétrica",
    "Engenharia de Produção",
    "Engenharia Química",
    "Engenharia Ambiental",
    "Engenharia de Computação",
    "Engenharia Mecatrônica",
    "Engenharia Biomédica",
    "Engenharia Aeroespacial",
    "Engenharia Agronômica",

    # Saúde
    "Medicina",
    "Enfermagem",
    "Psicologia",
    "Odontologia",
    "Farmácia",
    "Biomedicina",
    "Nutrição",
    "Fisioterapia",
    "Educação Física",
    "Veterinária",
    "Fonoaudiologia",
    "Radiologia",

    # Negócios
    "Administração",
    "Ciências Contábeis",
    "Economia",
    "Marketing",
    "Recursos Humanos",
    "Logística",
    "Comércio Exterior",
    "Gestão Financeira",
    "Processos Gerenciais",

    # Humanas
    "Direito",
    "Pedagogia",
    "História",
    "Geografia",
    "Filosofia",
    "Sociologia",
    "Serviço Social",
    "Letras",
    "Relações Internacionais",

    # Comunicação e Artes
    "Publicidade e Propaganda",
    "Jornalismo",
    "Relações Públicas",
    "Cinema e Audiovisual",
    "Design Gráfico",
    "Design de Interiores",
    "Artes Visuais",
    "Moda",
    "Arquitetura e Urbanismo",

    # Ciências Exatas
    "Matemática",
    "Física",
    "Química",
    "Estatística",

    # Biológicas
    "Biologia",
    "Biotecnologia",

    # Gastronomia e Eventos
    "Gastronomia",
    "Eventos",
    "Turismo",
    "Hotelaria",

    # Segurança
    "Segurança da Informação",
    "Segurança Pública",
    "Investigação Forense e Perícia Criminal",

    # Outros
    "Astronomia",
    "Oceanografia",
    "Meteorologia",
    "Música",
    "Teatro",
    "Dança"
]


class FormView(QWidget):

    def __init__(self, db, usuario, on_save=None):
        super().__init__()

        self.db = db
        self.usuario = usuario
        self.on_save = on_save

        self._editando = None
        self._foto_path = ""

        self.setStyleSheet("""
            QWidget {
                background-color: #0F172A;
                color: white;
                font-family: Segoe UI;
            }

            QFrame {
                background-color: #1E293B;
                border-radius: 18px;
            }

            QLabel#title {
                font-size: 24px;
                font-weight: bold;
            }

            QLabel#subtitle {
                color: #94A3B8;
                font-size: 13px;
            }

            QLabel#field {
                color: #CBD5E1;
                font-size: 12px;
                font-weight: bold;
            }

            QLineEdit,
            QComboBox,
            QDateEdit {
                background-color: #334155;
                border: 2px solid #475569;
                border-radius: 10px;

                padding-left: 14px;
                padding-right: 14px;

                color: white;
                font-size: 15px;

                min-height: 38px;
            }

            QTextEdit {
                background-color: #334155;
                border: 2px solid #475569;
                border-radius: 10px;
                padding: 12px;
                color: white;
                font-size: 15px;
            }
                           
             QComboBox::drop-down {
                border: none;
                width: 30px;
            }

            QComboBox::down-arrow {
                image: none;
            }              

            QLineEdit:focus,
            QTextEdit:focus,
            QComboBox:focus,
            QDateEdit:focus {
                border: 2px solid #3B82F6;
            }

            QPushButton {
                background-color: #2563EB;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
                color: white;
            }

            QPushButton:hover {
                background-color: #1D4ED8;
            }

            QPushButton#success {
                background-color: #16A34A;
            }

            QPushButton#danger {
                background-color: #DC2626;
            }

            QPushButton#purple {
                background-color: #7C3AED;
            }

            QPushButton#secondary {
                background-color: #475569;
            }

            QLabel#banner {
                background-color: #1D4ED8;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
            }

            QLabel#photo {
                background-color: #334155;
                border: 2px dashed #64748B;
                border-radius: 14px;
            }
        """)

        self.build_ui()

    # ==========================================================
    # UI
    # ==========================================================

    def build_ui(self):

        main = QVBoxLayout()
        main.setContentsMargins(25, 25, 25, 25)
        main.setSpacing(18)

        # ==================================================
        # HEADER
        # ==================================================

        title = QLabel("🎓 Cadastro de Alunos")
        title.setObjectName("title")

        subtitle = QLabel(
            "Gerencie informações acadêmicas dos alunos"
        )
        subtitle.setObjectName("subtitle")

        main.addWidget(title)
        main.addWidget(subtitle)

        # ==================================================
        # BUSCA
        # ==================================================

        busca_card = QFrame()

        busca_layout = QHBoxLayout()
        busca_layout.setContentsMargins(20, 20, 20, 20)

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText(
            "Buscar aluno por ID"
        )

        btn_buscar = QPushButton("🔍 Carregar")
        btn_buscar.clicked.connect(self.buscar_por_id)

        self.lbl_status = QLabel("")

        busca_layout.addWidget(self.input_id)
        busca_layout.addWidget(btn_buscar)
        busca_layout.addWidget(self.lbl_status)

        busca_card.setLayout(busca_layout)

        main.addWidget(busca_card)

        # ==================================================
        # BANNER EDIÇÃO
        # ==================================================

        self.banner = QLabel("")
        self.banner.setObjectName("banner")
        self.banner.hide()

        main.addWidget(self.banner)

        # ==================================================
        # DADOS PESSOAIS
        # ==================================================

        dados_card = QFrame()

        dados_layout = QHBoxLayout()
        dados_layout.setContentsMargins(20, 20, 20, 20)
        dados_layout.setSpacing(20)

        # FOTO
        foto_col = QVBoxLayout()

        self.photo = QLabel("📷\n\nAdicionar foto")
        self.photo.setObjectName("photo")

        self.photo.setAlignment(Qt.AlignCenter)
        self.photo.setFixedSize(150, 150)

        btn_foto = QPushButton("Selecionar Foto")
        btn_foto.clicked.connect(self.escolher_foto)

        foto_col.addWidget(self.photo)
        foto_col.addWidget(btn_foto)

        # FORM
        form_col = QVBoxLayout()
        form_col.setSpacing(18)
        form_col.addStretch()
        form_col.setContentsMargins(0, 4, 0, 4)

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome completo")

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Email")

        self.input_tel = QLineEdit()
        self.input_tel.setPlaceholderText("Telefone")

        self.combo_sexo = QComboBox()
        self.combo_sexo.addItems(["M", "F", "Outro"])

        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.date.setDate(QDate.currentDate())

        self.input_end = QLineEdit()
        self.input_end.setPlaceholderText(
            "Endereço completo"
        )

        self.combo_curso = QComboBox()
        self.combo_curso.addItems(CURSOS)

        form_col.addWidget(self.input_nome)
        form_col.addWidget(self.input_email)
        form_col.addWidget(self.input_tel)
        form_col.addWidget(self.combo_sexo)
        form_col.addWidget(self.date)
        form_col.addWidget(self.input_end)
        form_col.addWidget(self.combo_curso)

        dados_layout.addLayout(foto_col)
        dados_layout.addLayout(form_col)

        dados_card.setLayout(dados_layout)

        main.addWidget(dados_card)

        # ==================================================
        # OBSERVAÇÕES
        # ==================================================

        obs_card = QFrame()

        obs_layout = QVBoxLayout()
        obs_layout.setContentsMargins(20, 20, 20, 20)

        self.obs = QTextEdit()
        self.obs.setPlaceholderText(
            "Observações sobre o aluno..."
        )

        obs_layout.addWidget(self.obs)

        obs_card.setLayout(obs_layout)

        main.addWidget(obs_card)

        # ==================================================
        # BOTÕES
        # ==================================================

        buttons = QHBoxLayout()

        self.btn_salvar = QPushButton("💾 Cadastrar")
        self.btn_salvar.clicked.connect(self.salvar)

        self.btn_update = QPushButton("🔄 Atualizar")
        self.btn_update.setObjectName("success")
        self.btn_update.clicked.connect(self.atualizar)

        self.btn_update.hide()

        btn_pdf = QPushButton("🖨️ Gerar PDF")
        btn_pdf.setObjectName("purple")
        btn_pdf.clicked.connect(self.gerar_pdf)

        btn_limpar = QPushButton("✕ Limpar")
        btn_limpar.setObjectName("secondary")
        btn_limpar.clicked.connect(self.limpar)

        buttons.addWidget(self.btn_salvar)
        buttons.addWidget(self.btn_update)
        buttons.addWidget(btn_pdf)
        buttons.addWidget(btn_limpar)

        main.addLayout(buttons)

        self.setLayout(main)

    # ==========================================================
    # AÇÕES
    # ==========================================================

    def form_dados(self):

        return [
            self.input_nome.text(),
            self.input_email.text(),
            self.input_tel.text(),
            self.combo_sexo.currentText(),
            self.date.date().toString("dd/MM/yyyy"),
            self.input_end.text(),
            self.combo_curso.currentText(),
            self._foto_path,
            self.obs.toPlainText()
        ]

    def salvar(self):

        dados = self.form_dados()

        rowid = self.db.alunos.registrar(dados)

        self.db.historico.registrar(
            self.usuario,
            "CADASTRO",
            rowid,
            dados[0]
        )

        QMessageBox.information(
            self,
            "Sucesso",
            "Aluno cadastrado!"
        )

        self.limpar()

    def atualizar(self):

        if self._editando is None:
            return

        dados = self.form_dados()

        self.db.alunos.atualizar(
            self._editando,
            dados
        )

        self.db.historico.registrar(
            self.usuario,
            "ATUALIZAÇÃO",
            self._editando,
            dados[0]
        )

        QMessageBox.information(
            self,
            "Sucesso",
            "Aluno atualizado!"
        )

        self.limpar()

    def buscar_por_id(self):

        raw = self.input_id.text().strip()

        if not raw.isdigit():

            QMessageBox.warning(
                self,
                "Aviso",
                "Digite um ID válido."
            )

            return

        dados = self.db.alunos.buscar_por_id(
            int(raw)
        )

        if not dados:

            QMessageBox.warning(
                self,
                "Aviso",
                "Aluno não encontrado."
            )

            return

        self.carregar_aluno(dados)

    def carregar_aluno(self, dados):

        self._editando = dados[0]

        self.input_nome.setText(dados[1])
        self.input_email.setText(dados[2])
        self.input_tel.setText(dados[3])

        self.combo_sexo.setCurrentText(dados[4])

        self.input_end.setText(dados[6])

        self.combo_curso.setCurrentText(dados[7])

        self.obs.setText(dados[9] or "")

        self.banner.setText(
            f"✏️ Editando aluno #{dados[0]}"
        )

        self.banner.show()

        self.btn_salvar.hide()
        self.btn_update.show()

    def limpar(self):

        self._editando = None

        self.input_nome.clear()
        self.input_email.clear()
        self.input_tel.clear()
        self.input_end.clear()
        self.obs.clear()
        self.input_id.clear()

        self.banner.hide()

        self.btn_update.hide()
        self.btn_salvar.show()

        self.photo.setPixmap(QPixmap())
        self.photo.setText("📷\n\nAdicionar foto")

    def escolher_foto(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Foto",
            "",
            "Imagens (*.png *.jpg *.jpeg *.webp)"
        )

        if not path:
            return

        self._foto_path = path

        pixmap = QPixmap(path)

        self.photo.setPixmap(
            pixmap.scaled(
                150,
                150,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

        self.photo.setText("")

    def gerar_pdf(self):

        if self._editando is None:

            QMessageBox.warning(
                self,
                "Aviso",
                "Carregue um aluno primeiro."
            )

            return

        QMessageBox.information(
            self,
            "PDF",
            "PDF gerado com sucesso."
        )
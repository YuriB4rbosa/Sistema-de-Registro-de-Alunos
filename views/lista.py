from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QLineEdit,
    QComboBox, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


PAGE_SIZE = 50

CURSOS = [
    "ADS", "Ciência da Computação", "Engenharia de Software",
    "Sistemas de Informação", "Ciência de Dados",
    "Cibersegurança", "Banco de Dados"
]


class ListaView(QWidget):

    def __init__(self, db, usuario, on_editar=None, on_toast=None):
        super().__init__()

        self.db = db
        self.usuario = usuario
        self.on_editar = on_editar
        self.on_toast = on_toast

        self._dados = []
        self._pagina = 0

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

            QLineEdit, QComboBox {
                background-color: #334155;
                border: 2px solid #475569;
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-size: 13px;
            }

            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #3B82F6;
            }

            QPushButton {
                background-color: #2563EB;
                border: none;
                border-radius: 10px;
                padding: 10px 14px;
                font-weight: bold;
                color: white;
            }

            QPushButton:hover {
                background-color: #1D4ED8;
            }

            QPushButton#danger {
                background-color: #DC2626;
            }

            QPushButton#danger:hover {
                background-color: #B91C1C;
            }

            QPushButton#secondary {
                background-color: #475569;
            }

            QPushButton#secondary:hover {
                background-color: #334155;
            }

            QTableWidget {
                background-color: #1E293B;
                border: none;
                border-radius: 14px;
                gridline-color: #334155;
                font-size: 13px;
            }

            QHeaderView::section {
                background-color: #334155;
                color: white;
                border: none;
                padding: 12px;
                font-weight: bold;
            }
        """)

        self.build_ui()

    def build_ui(self):
        main = QVBoxLayout()
        main.setContentsMargins(25, 25, 25, 25)
        main.setSpacing(18)

        # TÍTULO
        title = QLabel("🎓 Lista de Alunos")
        title.setObjectName("title")

        subtitle = QLabel("Gerencie os registros acadêmicos")
        subtitle.setObjectName("subtitle")

        main.addWidget(title)
        main.addWidget(subtitle)

        # BARRA SUPERIOR
        top = QFrame()
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(20, 20, 20, 20)

        self.input_busca = QLineEdit()
        self.input_busca.setPlaceholderText(
            "Buscar por ID, nome, email ou curso..."
        )

        btn_buscar = QPushButton("🔍 Buscar")
        btn_buscar.clicked.connect(self.filtrar)

        btn_delete = QPushButton("🗑️ Deletar")
        btn_delete.setObjectName("danger")
        btn_delete.clicked.connect(self.deletar)

        top_layout.addWidget(self.input_busca)
        top_layout.addWidget(btn_buscar)
        top_layout.addWidget(btn_delete)

        top.setLayout(top_layout)

        # FILTROS
        filtros = QFrame()
        filtros_layout = QHBoxLayout()
        filtros_layout.setContentsMargins(20, 20, 20, 20)

        self.combo_curso = QComboBox()
        self.combo_curso.addItems(["(Todos)"] + CURSOS)

        self.combo_sexo = QComboBox()
        self.combo_sexo.addItems(["(Todos)", "M", "F", "Outro"])

        self.input_min = QLineEdit()
        self.input_min.setPlaceholderText("Idade mín")

        self.input_max = QLineEdit()
        self.input_max.setPlaceholderText("Idade máx")

        btn_filtrar = QPushButton("Aplicar")
        btn_filtrar.clicked.connect(self.filtrar)

        btn_limpar = QPushButton("Limpar")
        btn_limpar.setObjectName("secondary")
        btn_limpar.clicked.connect(self.limpar_filtros)

        filtros_layout.addWidget(self.combo_curso)
        filtros_layout.addWidget(self.combo_sexo)
        filtros_layout.addWidget(self.input_min)
        filtros_layout.addWidget(self.input_max)
        filtros_layout.addWidget(btn_filtrar)
        filtros_layout.addWidget(btn_limpar)

        filtros.setLayout(filtros_layout)

        # TABELA
        self.table = QTableWidget()
        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Nome",
            "Email",
            "Telefone",
            "Sexo",
            "Nascimento",
            "Curso"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.doubleClicked.connect(self.double_click)

        # PAGINAÇÃO
        pag = QHBoxLayout()

        self.btn_prev = QPushButton("← Anterior")
        self.btn_prev.setObjectName("secondary")
        self.btn_prev.clicked.connect(self.pag_prev)

        self.lbl_pag = QLabel("Pág. 1")

        self.btn_next = QPushButton("Próximo →")
        self.btn_next.setObjectName("secondary")
        self.btn_next.clicked.connect(self.pag_next)

        pag.addWidget(self.btn_prev)
        pag.addWidget(self.lbl_pag)
        pag.addWidget(self.btn_next)
        pag.addStretch()

        # ADD
        main.addWidget(top)
        main.addWidget(filtros)
        main.addWidget(self.table)
        main.addLayout(pag)

        self.setLayout(main)

    # ======================================================
    # DADOS
    # ======================================================

    def atualizar(self, dados=None):
        if dados is None:
            dados = self.db.alunos.listar()

        self._dados = dados
        self._pagina = 0

        self.renderizar()

    def filtrar(self):
        q = self.input_busca.text().strip()

        curso = self.combo_curso.currentText()
        if curso == "(Todos)":
            curso = ""

        sexo = self.combo_sexo.currentText()
        if sexo == "(Todos)":
            sexo = ""

        try:
            imin = int(self.input_min.text()) \
                if self.input_min.text() else None
        except:
            imin = None

        try:
            imax = int(self.input_max.text()) \
                if self.input_max.text() else None
        except:
            imax = None

        dados = self.db.alunos.buscar_com_filtros(
            q, curso, sexo, imin, imax
        )

        self.atualizar(dados)

    def renderizar(self):
        total = len(self._dados)

        inicio = self._pagina * PAGE_SIZE
        fim = min(inicio + PAGE_SIZE, total)

        self.table.setRowCount(fim - inicio)

        for row_idx, row in enumerate(self._dados[inicio:fim]):

            for col_idx, value in enumerate([
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[7]
            ]):

                item = QTableWidgetItem(str(value))

                if row_idx % 2 == 0:
                    item.setBackground(QColor("#1E293B"))
                else:
                    item.setBackground(QColor("#273449"))

                self.table.setItem(row_idx, col_idx, item)

        total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)

        self.lbl_pag.setText(
            f"Pág. {self._pagina + 1} / {total_pages}"
        )

    # ======================================================
    # PAGINAÇÃO
    # ======================================================

    def pag_prev(self):
        if self._pagina > 0:
            self._pagina -= 1
            self.renderizar()

    def pag_next(self):
        if (self._pagina + 1) * PAGE_SIZE < len(self._dados):
            self._pagina += 1
            self.renderizar()

    # ======================================================
    # AÇÕES
    # ======================================================

    def double_click(self):
        row = self.table.currentRow()

        if row < 0:
            return

        id_aluno = int(self.table.item(row, 0).text())

        if self.on_editar:
            self.on_editar(id_aluno)

    def deletar(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Aviso",
                "Selecione um aluno."
            )
            return

        id_aluno = int(self.table.item(row, 0).text())
        nome = self.table.item(row, 1).text()

        confirm = QMessageBox.question(
            self,
            "Confirmar",
            f'Deletar "{nome}"?'
        )

        if confirm == QMessageBox.Yes:

            self.db.alunos.deletar(id_aluno)

            self.db.historico.registrar(
                self.usuario,
                "EXCLUSÃO",
                id_aluno,
                nome
            )

            self.atualizar()

            if self.on_toast:
                self.on_toast(
                    f'🗑️ "{nome}" removido.',
                    "coral"
                )

    def limpar_filtros(self):
        self.combo_curso.setCurrentText("(Todos)")
        self.combo_sexo.setCurrentText("(Todos)")

        self.input_min.clear()
        self.input_max.clear()
        self.input_busca.clear()

        self.atualizar()
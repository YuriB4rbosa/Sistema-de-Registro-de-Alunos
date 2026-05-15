from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame,
    QTableWidget, QTableWidgetItem,
    QMessageBox, QComboBox, QHeaderView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class UsuariosView(QWidget):
    def __init__(self, db, usuario_atual):
        super().__init__()

        self.db = db
        self.usuario_atual = usuario_atual

        self.setStyleSheet("""
            QWidget {
                background-color: #0F172A;
                font-family: 'Segoe UI';
                color: white;
            }

            QFrame {
                background-color: #1E293B;
                border-radius: 18px;
            }

            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                color: white;
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
                padding: 12px;
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

            QLabel#status {
                font-size: 12px;
                color: #22C55E;
            }

            QTableWidget {
                background-color: #1E293B;
                border: none;
                border-radius: 12px;
                gridline-color: #334155;
                color: white;
                font-size: 13px;
            }

            QHeaderView::section {
                background-color: #334155;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)

        self.build_ui()
        self.atualizar()

    def build_ui(self):
        main = QVBoxLayout()
        main.setContentsMargins(30, 30, 30, 30)
        main.setSpacing(20)

        # Título
        title = QLabel("👥 Gerenciamento de Usuários")
        title.setObjectName("title")

        subtitle = QLabel("Somente administradores podem acessar")
        subtitle.setObjectName("subtitle")

        main.addWidget(title)
        main.addWidget(subtitle)

        # CARD CRIAR USUÁRIO
        card = QFrame()
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(15)

        form = QHBoxLayout()
        form.setSpacing(15)

        # Usuário
        col1 = QVBoxLayout()
        lbl_user = QLabel("Usuário")
        lbl_user.setObjectName("field")

        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Digite o usuário")

        col1.addWidget(lbl_user)
        col1.addWidget(self.input_user)

        # Senha
        col2 = QVBoxLayout()
        lbl_pass = QLabel("Senha")
        lbl_pass.setObjectName("field")

        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)
        self.input_pass.setPlaceholderText("Digite a senha")

        col2.addWidget(lbl_pass)
        col2.addWidget(self.input_pass)

        # Confirmar
        col3 = QVBoxLayout()
        lbl_conf = QLabel("Confirmar")
        lbl_conf.setObjectName("field")

        self.input_conf = QLineEdit()
        self.input_conf.setEchoMode(QLineEdit.Password)
        self.input_conf.setPlaceholderText("Confirme a senha")

        col3.addWidget(lbl_conf)
        col3.addWidget(self.input_conf)

        # Perfil
        col4 = QVBoxLayout()
        lbl_role = QLabel("Perfil")
        lbl_role.setObjectName("field")

        self.combo_role = QComboBox()
        self.combo_role.addItems(["user", "admin"])

        col4.addWidget(lbl_role)
        col4.addWidget(self.combo_role)

        form.addLayout(col1)
        form.addLayout(col2)
        form.addLayout(col3)
        form.addLayout(col4)

        card_layout.addLayout(form)

        # Status
        self.lbl_status = QLabel("")
        self.lbl_status.setObjectName("status")
        card_layout.addWidget(self.lbl_status)

        # Botões
        buttons = QHBoxLayout()

        btn_create = QPushButton("➕ Criar usuário")
        btn_create.clicked.connect(self.criar)

        btn_clear = QPushButton("✕ Limpar")
        btn_clear.setObjectName("secondary")
        btn_clear.clicked.connect(self.limpar)

        buttons.addWidget(btn_create)
        buttons.addWidget(btn_clear)

        card_layout.addLayout(buttons)

        card.setLayout(card_layout)

        # TABELA
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Usuário", "Perfil"])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Botão deletar
        btn_delete = QPushButton("🗑️ Remover selecionado")
        btn_delete.setObjectName("danger")
        btn_delete.clicked.connect(self.deletar)

        main.addWidget(card)
        main.addWidget(self.table)
        main.addWidget(btn_delete)

        self.setLayout(main)

    # ==========================================================
    # AÇÕES
    # ==========================================================

    def criar(self):
        u = self.input_user.text().strip()
        s = self.input_pass.text()
        c = self.input_conf.text()
        role = self.combo_role.currentText()

        if not u:
            self.status("Nome obrigatório", erro=True)
            return

        if len(s) < 6:
            self.status("Senha precisa ter 6+ caracteres", erro=True)
            return

        if s != c:
            self.status("As senhas não coincidem", erro=True)
            return

        ok = self.db.usuarios.criar(u, s, role)

        if ok:
            self.status(f"Usuário '{u}' criado com sucesso")
            self.limpar()
            self.atualizar()
        else:
            self.status("Usuário já existe", erro=True)

    def deletar(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um usuário.")
            return

        id_user = int(self.table.item(row, 0).text())
        nome = self.table.item(row, 1).text()
        role = self.table.item(row, 2).text()

        if nome == self.usuario_atual:
            QMessageBox.critical(
                self,
                "Erro",
                "Você não pode remover sua própria conta."
            )
            return

        if role == "admin":
            admins = [
                r for r in self.db.usuarios.listar()
                if r[2] == "admin"
            ]

            if len(admins) <= 1:
                QMessageBox.critical(
                    self,
                    "Erro",
                    "O sistema precisa de pelo menos 1 admin."
                )
                return

        confirm = QMessageBox.question(
            self,
            "Confirmar",
            f'Remover usuário "{nome}"?'
        )

        if confirm == QMessageBox.Yes:
            self.db.usuarios.deletar(id_user)
            self.atualizar()
            self.status(f"Usuário '{nome}' removido")

    def atualizar(self):
        usuarios = self.db.usuarios.listar()

        self.table.setRowCount(len(usuarios))

        for row_idx, row_data in enumerate(usuarios):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))

                if col_idx == 2:
                    if value == "admin":
                        item.setForeground(Qt.cyan)
                    else:
                        item.setForeground(Qt.lightGray)

                self.table.setItem(row_idx, col_idx, item)

    def limpar(self):
        self.input_user.clear()
        self.input_pass.clear()
        self.input_conf.clear()
        self.combo_role.setCurrentText("user")
        self.lbl_status.setText("")

    def status(self, msg, erro=False):
        if erro:
            self.lbl_status.setStyleSheet("color: #EF4444;")
        else:
            self.lbl_status.setStyleSheet("color: #22C55E;")

        self.lbl_status.setText(msg)
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys


class LoginWindow(QWidget):
    def __init__(self, db):
        super().__init__()

        self.db = db
        self.usuario_logado = None
        self.role = None

        self.setWindowTitle("Sistema Acadêmico")
        self.setFixedSize(430, 560)

        self.setStyleSheet("""
            QWidget {
                background-color: #0F172A;
                font-family: 'Segoe UI';
            }

            QFrame#card {
                background-color: #0F172A;
                border-radius: 20px;
            }

            QLabel#title {
                color: white;
                font-size: 28px;
                font-weight: bold;
            }

            QLabel#subtitle {
                color: #94A3B8;
                font-size: 13px;
            }

            QLabel#label {
                color: #ffffff;
                font-size: 12px;
                font-weight: bold;
            }

            QLineEdit {
                border: 2px solid #CBD5E1;
                border-radius: 12px;
                padding: 12px;
                font-size: 14px;
                background: #F8FAFC;
            }

            QLineEdit:focus {
                border: 2px solid #2563EB;
                background: white;
            }

            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 14px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1D4ED8;
            }

            QPushButton:pressed {
                background-color: #1E40AF;
            }

            QLabel#error {
                color: #DC2626;
                font-size: 12px;
            }
        """)

        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Ícone
        icon = QLabel("🎓")
        icon.setAlignment(Qt.AlignCenter)
        icon.setFont(QFont("Segoe UI Emoji", 42))

        title = QLabel("Sistema Acadêmico")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Registro de Alunos")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        # Card
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(15)

        # Usuário
        lbl_user = QLabel("Usuário")
        lbl_user.setObjectName("label")

        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Digite seu usuário")

        # Senha
        lbl_pass = QLabel("Senha")
        lbl_pass.setObjectName("label")

        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Digite sua senha")
        self.input_pass.setEchoMode(QLineEdit.Password)

        self.input_pass.returnPressed.connect(self.login)

        # Erro
        self.lbl_error = QLabel("")
        self.lbl_error.setObjectName("error")
        self.lbl_error.setAlignment(Qt.AlignCenter)

        # Botão
        btn_login = QPushButton("Entrar")
        btn_login.clicked.connect(self.login)

        # Adicionando ao card
        card_layout.addWidget(lbl_user)
        card_layout.addWidget(self.input_user)

        card_layout.addWidget(lbl_pass)
        card_layout.addWidget(self.input_pass)

        card_layout.addWidget(self.lbl_error)
        card_layout.addSpacing(10)
        card_layout.addWidget(btn_login)

        card.setLayout(card_layout)

        # Layout principal
        layout.addWidget(icon)
        layout.addSpacing(10)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(30)
        layout.addWidget(card)

        self.setLayout(layout)

    def login(self):
        u = self.input_user.text().strip()
        p = self.input_pass.text()

        if not u or not p:
            self.lbl_error.setText("Preencha usuário e senha.")
            return

        role = self.db.usuarios.login(u, p)

        if role:
            self.usuario_logado = u
            self.role = role
            self.close()
        else:
            self.lbl_error.setText("Usuário ou senha incorretos.")
            self.input_pass.clear()
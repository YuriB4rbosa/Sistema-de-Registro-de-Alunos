from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QFrame,
    QPushButton,
    QLabel,
    QMessageBox,
    QFileDialog,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
    QSizePolicy
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

import datetime

from views.dashboard import DashboardView
from views.form import FormView
from views.lista import ListaView
from views.historico import HistoricoView
from views.usuarios import UsuariosView

from services.exportacao import (
    exportar_excel,
    exportar_csv,
    fazer_backup
)


class AppWindow(QMainWindow):

    def __init__(self, db, usuario, role):

        super().__init__()

        self.db = db
        self.usuario = usuario
        self.role = role

        self.setWindowTitle(
            "Sistema de Registro de Alunos"
        )

        self.resize(1400, 820)

        self.setMinimumSize(1100, 700)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #0F172A;
            }

            QWidget {
                font-family: Segoe UI;
                color: white;
            }

            QFrame#sidebar {
                background-color: #111827;
                border-right: 1px solid #1E293B;
            }

            QFrame#header {
                background-color: #111827;
                border-bottom: 1px solid #1E293B;
            }

            QLabel#logo {
                font-size: 22px;
                font-weight: bold;
                color: white;
            }

            QLabel#small {
                color: #94A3B8;
                font-size: 12px;
            }

            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 12px;
                padding: 14px;
                text-align: left;
                font-size: 13px;
                color: #CBD5E1;
            }

            QPushButton:hover {
                background-color: #1E293B;
            }

            QPushButton#active {
                background-color: #2563EB;
                color: white;
                font-weight: bold;
            }

            QPushButton#danger {
                background-color: #DC2626;
                color: white;
                text-align: center;
            }

            QPushButton#tool {
                background-color: #1E293B;
                text-align: center;
            }

            QPushButton#tool:hover {
                background-color: #334155;
            }
                           
            QMessageBox {
                background-color: #111827;
            }

            QMessageBox QLabel {
                color: white;
                font-size: 13px;
            }

            QMessageBox QPushButton {
                background-color: #2563EB;
                color: white;

                border: none;
                border-radius: 8px;

                padding: 8px 18px;
                min-width: 80px;
            }

            QMessageBox QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)

        self.build_ui()

    # ==========================================================
    # UI
    # ==========================================================

    def build_ui(self):

        root = QWidget()

        self.setCentralWidget(root)

        main_layout = QHBoxLayout(root)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ==================================================
        # SIDEBAR
        # ==================================================

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")

        sidebar.setFixedWidth(260)

        side_layout = QVBoxLayout()

        side_layout.setContentsMargins(18, 18, 18, 18)

        side_layout.setSpacing(8)

        logo = QLabel("🎓 Sistema Acadêmico")
        logo.setObjectName("logo")

        subtitle = QLabel(
            "Registro de Alunos"
        )

        subtitle.setObjectName("small")

        side_layout.addWidget(logo)
        side_layout.addWidget(subtitle)

        side_layout.addSpacing(20)

        self.nav_buttons = {}

        navs = [
            ("dashboard", "📊 Dashboard"),
            ("form", "✏️ Cadastrar"),
            ("list", "📋 Alunos"),
            ("history", "🕓 Histórico")
        ]

        if self.role == "admin":
            navs.append(
                ("users", "👥 Usuários")
            )

        for key, text in navs:

            btn = QPushButton(text)

            btn.clicked.connect(
                lambda _, k=key: self.show_view(k)
            )

            side_layout.addWidget(btn)

            self.nav_buttons[key] = btn

        side_layout.addSpacing(25)

        tools = [
            ("📤 Exportar Excel", self.exportar_excel),
            ("📤 Exportar CSV", self.exportar_csv),
            ("💾 Backup", self.fazer_backup),
            ("🗑️ Limpar formulário", self.limpar_form)
        ]

        for text, func in tools:

            btn = QPushButton(text)

            btn.setObjectName("tool")

            btn.clicked.connect(func)

            side_layout.addWidget(btn)

        side_layout.addStretch()

        user_box = QLabel(
            f"👤 {self.usuario}\nPerfil: {self.role}"
        )

        user_box.setStyleSheet("""
            background-color: #1E293B;
            border-radius: 14px;
            padding: 14px;
            color: white;
        """)

        side_layout.addWidget(user_box)

        sair = QPushButton("Sair")
        sair.setObjectName("danger")

        sair.clicked.connect(self.close)

        side_layout.addWidget(sair)

        sidebar.setLayout(side_layout)

        # ==================================================
        # CONTAINER
        # ==================================================

        container = QWidget()

        container_layout = QVBoxLayout(container)

        container_layout.setContentsMargins(0, 0, 0, 0)

        # ==================================================
        # HEADER
        # ==================================================

        header = QFrame()

        header.setObjectName("header")

        header.setFixedHeight(70)

        header_layout = QHBoxLayout(header)

        header_layout.setContentsMargins(
            24,
            0,
            24,
            0
        )

        self.lbl_title = QLabel("Dashboard")

        self.lbl_title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)

        self.lbl_count = QLabel("0 alunos")

        self.lbl_count.setStyleSheet("""
            color: #94A3B8;
            font-size: 13px;
        """)

        header_layout.addWidget(self.lbl_title)

        header_layout.addStretch()

        header_layout.addWidget(self.lbl_count)

        # ==================================================
        # STACK
        # ==================================================

        self.stack = QStackedWidget()

        self.view_dashboard = DashboardView(self.db)

        self.view_form = FormView(
            self.db,
            self.usuario,
            on_save=self.on_form_save
        )

        self.view_list = ListaView(
            self.db,
            self.usuario
        )

        self.view_history = HistoricoView(
            self.db
        )

        self.view_users = UsuariosView(
            self.db,
            self.usuario
        )

        self.views = {
            "dashboard": self.view_dashboard,
            "form": self.view_form,
            "list": self.view_list,
            "history": self.view_history,
            "users": self.view_users
        }

        self.stack.addWidget(
            self.view_dashboard
        )

        self.stack.addWidget(
            self.view_form
        )

        self.stack.addWidget(
            self.view_list
        )

        self.stack.addWidget(
            self.view_history
        )

        if self.role == "admin":

            self.stack.addWidget(
                self.view_users
            )

        container_layout.addWidget(header)
        container_layout.addWidget(self.stack)

        # ==================================================
        # FINAL
        # ==================================================

        main_layout.addWidget(sidebar)
        main_layout.addWidget(container)

        self.show_view("dashboard")

    # ==========================================================
    # VIEW
    # ==========================================================

    def show_view(self, key):

        if key == "users" and self.role != "admin":
            return

        view = self.views[key]

        self.stack.setCurrentWidget(view)

        self.lbl_title.setText(
            key.capitalize()
        )

        for k, btn in self.nav_buttons.items():

            if k == key:
                btn.setObjectName("active")
            else:
                btn.setObjectName("")

            btn.style().unpolish(btn)
            btn.style().polish(btn)

        # refresh

        try:
            view.atualizar()
        except:
            pass

        self.update_count()

    # ==========================================================
    # CALLBACKS
    # ==========================================================

    def on_form_save(self, msg="", kind="verde"):

        self.update_count()

        QMessageBox.information(
            self,
            "Sucesso",
            msg or "Operação realizada."
        )

    def limpar_form(self):

        self.view_form.limpar()

        self.show_view("form")

    def update_count(self):

        n = self.db.alunos.contar()

        self.lbl_count.setText(
            f"{n} aluno(s)"
        )

    # ==========================================================
    # EXPORT
    # ==========================================================

    def exportar_excel(self):

        dados = self.db.alunos.listar()

        if not dados:

            QMessageBox.warning(
                self,
                "Aviso",
                "Nenhum aluno encontrado."
            )

            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Excel",
            f"alunos_{datetime.date.today()}.xlsx",
            "Excel (*.xlsx)"
        )

        if not path:
            return

        exportar_excel(dados, path)

        QMessageBox.information(
            self,
            "Sucesso",
            "Excel exportado!"
        )

    def exportar_csv(self):

        dados = self.db.alunos.listar()

        if not dados:

            QMessageBox.warning(
                self,
                "Aviso",
                "Nenhum aluno encontrado."
            )

            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar CSV",
            f"alunos_{datetime.date.today()}.csv",
            "CSV (*.csv)"
        )

        if not path:
            return

        exportar_csv(dados, path)

        QMessageBox.information(
            self,
            "Sucesso",
            "CSV exportado!"
        )

    def fazer_backup(self):

        try:

            fazer_backup()

            QMessageBox.information(
                self,
                "Backup",
                "Backup realizado!"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    # ==========================================================
    # CLOSE
    # ==========================================================

    def closeEvent(self, event):

        confirm = QMessageBox.question(
            self,
            "Sair",
            "Deseja realmente sair?"
        )

        if confirm == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
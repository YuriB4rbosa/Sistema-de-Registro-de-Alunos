from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class HistoricoView(QWidget):

    def __init__(self, db):
        super().__init__()

        self.db = db

        self.setStyleSheet("""
            QWidget {
                background-color: #0F172A;
                color: white;
                font-family: 'Segoe UI';
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

            QFrame {
                background-color: #1E293B;
                border-radius: 18px;
            }

            QTableWidget {
                background-color: #1E293B;
                border: none;
                border-radius: 14px;
                gridline-color: #334155;
                font-size: 13px;
                color: white;
            }

            QHeaderView::section {
                background-color: #334155;
                color: white;
                border: none;
                padding: 12px;
                font-weight: bold;
            }

            QScrollBar:vertical {
                background: #1E293B;
                width: 10px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background: #475569;
                border-radius: 5px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background: #64748B;
            }
        """)

        self.build_ui()

    def build_ui(self):

        main = QVBoxLayout()
        main.setContentsMargins(25, 25, 25, 25)
        main.setSpacing(18)

        # ==================================================
        # TÍTULO
        # ==================================================

        title = QLabel("📜 Histórico de Alterações")
        title.setObjectName("title")

        subtitle = QLabel(
            "Registro completo das ações realizadas no sistema"
        )
        subtitle.setObjectName("subtitle")

        main.addWidget(title)
        main.addWidget(subtitle)

        # ==================================================
        # CARD DA TABELA
        # ==================================================

        card = QFrame()

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(20, 20, 20, 20)

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "Data/Hora",
            "Usuário",
            "Ação",
            "ID",
            "Aluno",
            "Detalhes"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.verticalHeader().setVisible(False)

        card_layout.addWidget(self.table)

        card.setLayout(card_layout)

        main.addWidget(card)

        self.setLayout(main)

    # ======================================================
    # ATUALIZAR TABELA
    # ======================================================

    def atualizar(self):

        historico = self.db.historico.listar()

        self.table.setRowCount(len(historico))

        for row_idx, row in enumerate(historico):

            acao = row[2]

            for col_idx, value in enumerate(row):

                item = QTableWidgetItem(str(value))

                # Zebra rows
                if row_idx % 2 == 0:
                    item.setBackground(QColor("#1E293B"))
                else:
                    item.setBackground(QColor("#273449"))

                # Cores das ações
                if acao == "CADASTRO":
                    item.setForeground(QColor("#22C55E"))

                elif acao == "ATUALIZAÇÃO":
                    item.setForeground(QColor("#3B82F6"))

                elif acao == "EXCLUSÃO":
                    item.setForeground(QColor("#EF4444"))

                elif acao == "PDF":
                    item.setForeground(QColor("#A855F7"))

                self.table.setItem(
                    row_idx,
                    col_idx,
                    item
                )
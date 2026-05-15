from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QGridLayout,
    QProgressBar,
    QSizePolicy
)

from PySide6.QtCore import Qt

from PySide6.QtGui import QColor


class DashboardView(QWidget):

    def __init__(self, db):
        super().__init__()

        self.db = db

        self.setStyleSheet("""
            QWidget {
                
                color: white;
                font-family: Segoe UI;
            }

            QLabel#title {
                font-size: 28px;
                font-weight: bold;
            }

            QLabel#subtitle {
                color: #94A3B8;
                font-size: 13px;
            }

            QFrame#card {
                background-color: #1E293B;
                border-radius: 18px;
            }

            QLabel#statIcon {
                font-size: 28px;
            }

            QLabel#statNumber {
                font-size: 26px;
                font-weight: bold;
                color: white;
            }

            QLabel#statLabel {
                color: #94A3B8;
                font-size: 12px;
            }

            QLabel#sectionTitle {
                font-size: 18px;
                font-weight: bold;
            }

            QLabel#courseName {
                color: white;
                font-size: 13px;
            }

            QLabel#courseCount {
                color: #94A3B8;
                font-size: 12px;
                font-weight: bold;
            }

            QLabel#recentName {
                font-size: 13px;
                font-weight: bold;
                color: white;
            }

            QLabel#recentCourse {
                color: #94A3B8;
                font-size: 12px;
            }

            QProgressBar {
                border: none;
                background-color: #334155;
                border-radius: 8px;
                height: 12px;
                text-align: center;
            }

            QProgressBar::chunk {
                border-radius: 8px;
                background-color: #3B82F6;
            }
        """)

        self.build_ui()

    # ======================================================
    # UI
    # ======================================================

    def build_ui(self):

        self.main = QVBoxLayout()
        self.main.setContentsMargins(25, 25, 25, 25)
        self.main.setSpacing(20)

        # ==================================================
        # HEADER
        # ==================================================

        title = QLabel("📊 Dashboard")
        title.setObjectName("title")

        subtitle = QLabel(
            "Visão geral do sistema acadêmico"
        )
        subtitle.setObjectName("subtitle")

        self.main.addWidget(title)
        self.main.addWidget(subtitle)

        # ==================================================
        # STATS
        # ==================================================

        stats_layout = QGridLayout()
        stats_layout.setSpacing(14)

        self.stats = {}

        stats_cfg = [
            ("total", "🎓", "Total de Alunos"),
            ("masculino", "♂", "Masculino"),
            ("feminino", "♀", "Feminino"),
            ("cursos", "📚", "Cursos"),
            ("idade", "📅", "Idade Média"),
            ("novos", "✨", "Novos no mês")
        ]

        for idx, (key, icon, label) in enumerate(stats_cfg):

            card = QFrame()
            card.setObjectName("card")

            card_layout = QVBoxLayout()
            card_layout.setContentsMargins(20, 20, 20, 20)

            lbl_icon = QLabel(icon)
            lbl_icon.setObjectName("statIcon")
            lbl_icon.setAlignment(Qt.AlignCenter)

            lbl_number = QLabel("0")
            lbl_number.setObjectName("statNumber")
            lbl_number.setAlignment(Qt.AlignCenter)

            lbl_text = QLabel(label)
            lbl_text.setObjectName("statLabel")
            lbl_text.setAlignment(Qt.AlignCenter)

            card_layout.addWidget(lbl_icon)
            card_layout.addWidget(lbl_number)
            card_layout.addWidget(lbl_text)

            card.setLayout(card_layout)

            stats_layout.addWidget(
                card,
                idx // 3,
                idx % 3
            )

            self.stats[key] = lbl_number

        self.main.addLayout(stats_layout)

        # ==================================================
        # TOP CURSOS
        # ==================================================

        self.top_card = QFrame()
        self.top_card.setObjectName("card")

        top_layout = QVBoxLayout()
        top_layout.setContentsMargins(20, 20, 20, 20)

        top_title = QLabel("📚 Top Cursos")
        top_title.setObjectName("sectionTitle")

        top_layout.addWidget(top_title)

        self.top_container = QVBoxLayout()
        self.top_container.setSpacing(14)

        top_layout.addLayout(self.top_container)

        self.top_card.setLayout(top_layout)

        self.main.addWidget(self.top_card)

        # ==================================================
        # ÚLTIMOS ALUNOS
        # ==================================================

        self.rec_card = QFrame()
        self.rec_card.setObjectName("card")

        rec_layout = QVBoxLayout()
        rec_layout.setContentsMargins(20, 20, 20, 20)

        rec_title = QLabel("🕓 Últimos Alunos")
        rec_title.setObjectName("sectionTitle")

        rec_layout.addWidget(rec_title)

        self.rec_container = QVBoxLayout()
        self.rec_container.setSpacing(12)

        rec_layout.addLayout(self.rec_container)

        self.rec_card.setLayout(rec_layout)

        self.main.addWidget(self.rec_card)

        self.setLayout(self.main)

    # ======================================================
    # ATUALIZAR
    # ======================================================

    def atualizar(self):

        total = self.db.alunos.contar()

        sexos = self.db.alunos.stats_por_sexo()

        cursos = self.db.alunos.stats_por_curso()

        idade = self.db.alunos.media_idade()

        novos = self.db.historico.novos_este_mes()

        # ==================================================
        # STATS
        # ==================================================

        self.stats["total"].setText(str(total))

        self.stats["masculino"].setText(
            str(sexos.get("M", 0))
        )

        self.stats["feminino"].setText(
            str(sexos.get("F", 0))
        )

        self.stats["cursos"].setText(
            str(len(cursos))
        )

        self.stats["idade"].setText(
            f"{idade} a"
        )

        self.stats["novos"].setText(
            str(novos)
        )

        # ==================================================
        # LIMPAR LAYOUTS
        # ==================================================

        self.clear_layout(self.top_container)
        self.clear_layout(self.rec_container)

        # ==================================================
        # TOP CURSOS
        # ==================================================

        if cursos:

            max_c = cursos[0][1]

            for curso, cnt in cursos:

                row = QVBoxLayout()

                top = QHBoxLayout()

                lbl_name = QLabel(curso)
                lbl_name.setObjectName("courseName")

                lbl_count = QLabel(str(cnt))
                lbl_count.setObjectName("courseCount")

                top.addWidget(lbl_name)
                top.addStretch()
                top.addWidget(lbl_count)

                progress = QProgressBar()

                progress.setMaximum(max_c)
                progress.setValue(cnt)

                row.addLayout(top)
                row.addWidget(progress)

                self.top_container.addLayout(row)

        # ==================================================
        # ÚLTIMOS ALUNOS
        # ==================================================

        ultimos = self.db.alunos.ultimos(5)

        if ultimos:

            for row in ultimos:

                card = QFrame()
                card.setObjectName("card")

                layout = QHBoxLayout()
                layout.setContentsMargins(16, 16, 16, 16)

                left = QVBoxLayout()

                lbl_name = QLabel(
                    f"#{row[0]} • {row[1]}"
                )

                lbl_name.setObjectName("recentName")

                lbl_course = QLabel(row[7])
                lbl_course.setObjectName("recentCourse")

                left.addWidget(lbl_name)
                left.addWidget(lbl_course)

                layout.addLayout(left)

                card.setLayout(layout)

                self.rec_container.addWidget(card)

        else:

            empty = QLabel(
                "Nenhum aluno cadastrado."
            )

            empty.setObjectName("subtitle")

            self.rec_container.addWidget(empty)

    # ======================================================
    # UTIL
    # ======================================================

    def clear_layout(self, layout):

        while layout.count():

            item = layout.takeAt(0)

            widget = item.widget()

            child_layout = item.layout()

            if widget:
                widget.deleteLater()

            elif child_layout:
                self.clear_layout(child_layout)
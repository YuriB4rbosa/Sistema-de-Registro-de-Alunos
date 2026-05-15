import sys
import os

from PySide6.QtWidgets import QApplication

sys.path.insert(
    0,
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

from database import db

from views.login import LoginWindow
from views.app import AppWindow


def main():

    app = QApplication(sys.argv)

    # ======================================================
    # LOGIN
    # ======================================================

    login = LoginWindow(db)

    login.show()

    app.exec()

    # ======================================================
    # APP PRINCIPAL
    # ======================================================

    if login.usuario_logado:

        window = AppWindow(
            db,
            login.usuario_logado,
            login.role
        )

        window.show()

        sys.exit(app.exec())


if __name__ == "__main__":
    main()
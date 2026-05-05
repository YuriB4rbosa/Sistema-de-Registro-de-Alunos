import sys
import os


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database   import db
from views.login import LoginWindow
from views.app   import AppWindow


def main():
    
    login = LoginWindow(db)
    login.mainloop()

    
    if login.usuario_logado:
        app = AppWindow(db, login.usuario_logado, login.role)
        app.mainloop()


if __name__ == "__main__":
    main()
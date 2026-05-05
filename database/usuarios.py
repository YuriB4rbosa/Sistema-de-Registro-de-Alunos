import bcrypt
import sqlite3


class UsuariosRepository:
    def __init__(self, conn):
        self.conn = conn
        self.c    = conn.cursor()

    def seed_admin(self):
        self.c.execute("SELECT id FROM usuarios WHERE username = 'admin'")
        if not self.c.fetchone():
            senha_hash = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()
            self.c.execute(
                "INSERT INTO usuarios(username, senha, role) VALUES (?,?,?)",
                ("admin", senha_hash, "admin"))
            self.conn.commit()

    def login(self, username, senha):
        self.c.execute(
            "SELECT senha, role FROM usuarios WHERE username=?", (username,))
        row = self.c.fetchone()
        if not row:
            return None
        if bcrypt.checkpw(senha.encode(), row[0].encode()):
            return row[1]
        return None

    def criar(self, username, senha, role="user"):
        try:
            h = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
            self.c.execute(
                "INSERT INTO usuarios(username, senha, role) VALUES (?,?,?)",
                (username, h, role))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def listar(self):
        self.c.execute("SELECT id, username, role FROM usuarios")
        return self.c.fetchall()

    def deletar(self, id):
        self.c.execute("DELETE FROM usuarios WHERE id=?", (id,))
        self.conn.commit()
from .connection import get_connection, criar_tabelas
from .alunos    import AlunosRepository
from .usuarios  import UsuariosRepository
from .historico import HistoricoRepository


class Database:
    """Ponto único de acesso ao banco de dados."""
    def __init__(self):
        self.conn     = get_connection()
        criar_tabelas(self.conn)
        self.alunos   = AlunosRepository(self.conn)
        self.usuarios = UsuariosRepository(self.conn)
        self.historico = HistoricoRepository(self.conn)
        self.usuarios.seed_admin()


db = Database()
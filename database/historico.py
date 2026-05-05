import datetime


class HistoricoRepository:
    def __init__(self, conn):
        self.conn = conn
        self.c    = conn.cursor()

    def registrar(self, usuario, acao, aluno_id=None,
                  aluno_nome=None, detalhes=None):
        agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.c.execute(
            "INSERT INTO historico(usuario,acao,aluno_id,aluno_nome,detalhes,data_hora) "
            "VALUES(?,?,?,?,?,?)",
            (usuario, acao, aluno_id, aluno_nome, detalhes, agora))
        self.conn.commit()

    def listar(self, limit=200):
        self.c.execute(
            "SELECT data_hora,usuario,acao,aluno_id,aluno_nome,detalhes "
            "FROM historico ORDER BY id DESC LIMIT ?", (limit,))
        return self.c.fetchall()

    def novos_este_mes(self):
        mes = datetime.date.today().strftime("%m/%Y")
        self.c.execute(
            "SELECT COUNT(*) FROM historico "
            "WHERE acao='CADASTRO' AND detalhes LIKE ?",
            (f"%{mes}%",))
        return self.c.fetchone()[0]
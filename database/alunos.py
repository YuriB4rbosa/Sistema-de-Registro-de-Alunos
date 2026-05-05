import datetime


class AlunosRepository:
    def __init__(self, conn):
        self.conn = conn
        self.c    = conn.cursor()

    def registrar(self, dados):
        self.c.execute(
            "INSERT INTO estudantes(name,email,telefone,sexo,"
            "data_nascimento,endereco,curso,imagem_aluno,observacoes) VALUES(?,?,?,?,?,?,?,?,?)",
            dados)
        self.conn.commit()
        return self.c.lastrowid

    def listar(self):
        self.c.execute(
            "SELECT id,name,email,telefone,sexo,data_nascimento,endereco,curso "
            "FROM estudantes ORDER BY name")
        return self.c.fetchall()

    def buscar_por_id(self, id):
        self.c.execute("SELECT id,name,email,telefone,sexo,data_nascimento,"
                       "endereco,curso,imagem_aluno,observacoes FROM estudantes WHERE id=?", (id,))
        return self.c.fetchone()

    def buscar_por_texto(self, texto):
        q = f"%{texto}%"
        self.c.execute(
            "SELECT id,name,email,telefone,sexo,data_nascimento,endereco,curso "
            "FROM estudantes WHERE CAST(id AS TEXT) LIKE ? OR name LIKE ? "
            "OR email LIKE ? OR curso LIKE ? OR telefone LIKE ?",
            (q, q, q, q, q))
        return self.c.fetchall()

    def buscar_com_filtros(self, texto="", curso="", sexo="",
                            idade_min=None, idade_max=None):
        sql    = ("SELECT id,name,email,telefone,sexo,data_nascimento,endereco,curso "
                  "FROM estudantes WHERE 1=1")
        params = []
        if texto:
            q = f"%{texto}%"
            sql += (" AND (CAST(id AS TEXT) LIKE ? OR name LIKE ? "
                    "OR email LIKE ? OR telefone LIKE ?)")
            params += [q, q, q, q]
        if curso:
            sql += " AND curso = ?"
            params.append(curso)
        if sexo:
            sql += " AND sexo = ?"
            params.append(sexo)
        if idade_min is not None:
            ano_max = datetime.date.today().year - idade_min
            sql += " AND CAST(substr(data_nascimento,7,4) AS INTEGER) <= ?"
            params.append(ano_max)
        if idade_max is not None:
            ano_min = datetime.date.today().year - idade_max
            sql += " AND CAST(substr(data_nascimento,7,4) AS INTEGER) >= ?"
            params.append(ano_min)
        sql += " ORDER BY name"
        self.c.execute(sql, params)
        return self.c.fetchall()

    def atualizar(self, id, dados):
        self.c.execute(
            """UPDATE estudantes SET name=?,email=?,telefone=?,sexo=?,
               data_nascimento=?,endereco=?,curso=?,imagem_aluno=?,observacoes=?
               WHERE id=?""",
            (*dados, id))
        self.conn.commit()

    def deletar(self, id):
        self.c.execute("DELETE FROM estudantes WHERE id=?", (id,))
        self.conn.commit()

    def contar(self):
        self.c.execute("SELECT COUNT(*) FROM estudantes")
        return self.c.fetchone()[0]

    def stats_por_sexo(self):
        self.c.execute("SELECT sexo, COUNT(*) FROM estudantes GROUP BY sexo")
        return dict(self.c.fetchall())

    def stats_por_curso(self):
        self.c.execute(
            "SELECT curso, COUNT(*) FROM estudantes "
            "GROUP BY curso ORDER BY COUNT(*) DESC LIMIT 10")
        return self.c.fetchall()

    def media_idade(self):
        self.c.execute(
            "SELECT AVG(CAST(strftime('%Y','now') AS INTEGER) - "
            "CAST(substr(data_nascimento,7,4) AS INTEGER)) FROM estudantes "
            "WHERE length(data_nascimento) >= 10")
        r = self.c.fetchone()[0]
        return round(r, 1) if r else 0

    def ultimos(self, n=5):
        self.c.execute(
            "SELECT id,name,email,telefone,sexo,data_nascimento,endereco,curso "
            "FROM estudantes ORDER BY id DESC LIMIT ?", (n,))
        return self.c.fetchall()
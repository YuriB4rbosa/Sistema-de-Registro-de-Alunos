import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(BASE_DIR, "estudante.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn


def criar_tabelas(conn):
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS estudantes (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT NOT NULL,
            email           TEXT NOT NULL,
            telefone        TEXT NOT NULL,
            sexo            TEXT NOT NULL,
            data_nascimento TEXT NOT NULL,
            endereco        TEXT NOT NULL,
            curso           TEXT NOT NULL,
            imagem_aluno    TEXT,
            observacoes     TEXT
        );

        CREATE TABLE IF NOT EXISTS usuarios (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            senha    TEXT NOT NULL,
            role     TEXT NOT NULL DEFAULT "user"
        );

        CREATE TABLE IF NOT EXISTS historico (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario    TEXT NOT NULL,
            acao       TEXT NOT NULL,
            aluno_id   INTEGER,
            aluno_nome TEXT,
            detalhes   TEXT,
            data_hora  TEXT NOT NULL
        );
    ''')
    conn.commit()

    
    try:
        conn.execute("ALTER TABLE estudantes ADD COLUMN observacoes TEXT")
        conn.commit()
    except Exception:
        pass  # coluna já existe
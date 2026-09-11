import sqlite3


def conectar():
    conexao = sqlite3.connect("atendeai.db")
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            identificador TEXT UNIQUE,
            canal TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            mensagem TEXT NOT NULL,
            remetente TEXT NOT NULL,
            data DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (cliente_id)
            REFERENCES clientes(id)
        )
    """)

    conexao.commit()
    conexao.close()


def buscar_ou_criar_cliente(nome, identificador, canal):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM clientes WHERE identificador = ?",
        (identificador,)
    )

    cliente = cursor.fetchone()

    if cliente:
        cliente_id = cliente["id"]
        conexao.close()
        return cliente_id

    cursor.execute("""
        INSERT INTO clientes (nome, identificador, canal)
        VALUES (?, ?, ?)
    """, (nome, identificador, canal))

    conexao.commit()

    cliente_id = cursor.lastrowid

    conexao.close()

    return cliente_id


def salvar_mensagem(cliente_id, mensagem, remetente):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO mensagens (
            cliente_id,
            mensagem,
            remetente
        )
        VALUES (?, ?, ?)
    """, (
        cliente_id,
        mensagem,
        remetente
    ))

    conexao.commit()
    conexao.close()
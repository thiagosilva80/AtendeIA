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
# Verifica se a coluna modo_atendimento já existe
    cursor.execute("PRAGMA table_info(clientes)")

    colunas = cursor.fetchall()

    nomes_colunas = [
            coluna["name"] for coluna in colunas
        ]

    if "modo_atendimento" not in nomes_colunas:

            cursor.execute("""
                ALTER TABLE clientes
                ADD COLUMN modo_atendimento TEXT DEFAULT 'ia'
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
    
def buscar_historico(cliente_id, limite=10):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT mensagem, remetente, data
        FROM mensagens
        WHERE cliente_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (cliente_id, limite))

    mensagens = cursor.fetchall()

    conexao.close()

    # Como buscamos do mais recente para o mais antigo,
    # vamos inverter para ficar na ordem correta.
    mensagens = list(reversed(mensagens))

    return mensagens

def listar_clientes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            clientes.id,
            clientes.nome,
            clientes.identificador,
            clientes.canal,
            clientes.modo_atendimento,
            (
                SELECT mensagem
                FROM mensagens
                WHERE mensagens.cliente_id = clientes.id
                ORDER BY mensagens.id DESC
                LIMIT 1
            ) AS ultima_mensagem
        FROM clientes
        ORDER BY clientes.id DESC
    """)

    clientes = cursor.fetchall()

    conexao.close()

    return clientes

def buscar_todas_mensagens(cliente_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            mensagem,
            remetente,
            data
        FROM mensagens
        WHERE cliente_id = ?
        ORDER BY id ASC
    """, (cliente_id,))

    mensagens = cursor.fetchall()

    conexao.close()

    return mensagens

def alterar_modo_atendimento(cliente_id, modo):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE clientes
        SET modo_atendimento = ?
        WHERE id = ?
    """, (modo, cliente_id))

    conexao.commit()
    conexao.close()


def buscar_modo_atendimento(cliente_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT modo_atendimento
        FROM clientes
        WHERE id = ?
    """, (cliente_id,))

    cliente = cursor.fetchone()

    conexao.close()

    if cliente:
        return cliente["modo_atendimento"]

    return "ia"
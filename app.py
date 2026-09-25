from flask import Flask, jsonify, request, render_template

from atendimento import processar_mensagem

from database import (
    criar_tabelas,
    buscar_ou_criar_cliente,
    salvar_mensagem,
    buscar_historico,
    listar_clientes,
    buscar_todas_mensagens,
    alterar_modo_atendimento,
    buscar_modo_atendimento
)


app = Flask(__name__)

criar_tabelas()


# ==========================================
# PÁGINA PRINCIPAL
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# LISTAR CLIENTES
# ==========================================

@app.route("/api/clientes")
def api_clientes():

    clientes = listar_clientes()

    resultado = []

    for cliente in clientes:

        resultado.append({
            "id": cliente["id"],
            "nome": cliente["nome"],
            "identificador": cliente["identificador"],
            "canal": cliente["canal"],
            "ultima_mensagem": cliente["ultima_mensagem"],
            "modo_atendimento": cliente["modo_atendimento"]
        })

    return jsonify(resultado)


# ==========================================
# HISTÓRICO DE UM CLIENTE
# ==========================================

@app.route("/api/clientes/<int:cliente_id>/mensagens")
def api_mensagens_cliente(cliente_id):

    mensagens = buscar_todas_mensagens(cliente_id)

    resultado = []

    for mensagem in mensagens:

        resultado.append({
            "id": mensagem["id"],
            "mensagem": mensagem["mensagem"],
            "remetente": mensagem["remetente"],
            "data": mensagem["data"]
        })

    return jsonify(resultado)


# ==========================================
# ALTERAR MODO IA / HUMANO
# ==========================================

@app.route(
    "/api/clientes/<int:cliente_id>/modo",
    methods=["POST"]
)
def alterar_modo_cliente(cliente_id):

    dados = request.get_json()

    modo = dados.get("modo")

    if modo not in ["ia", "humano"]:

        return jsonify({
            "erro": "Modo de atendimento inválido"
        }), 400

    alterar_modo_atendimento(
        cliente_id,
        modo
    )

    return jsonify({
        "cliente_id": cliente_id,
        "modo": modo
    })


# ==========================================
# RECEBER MENSAGEM DO CLIENTE
# ==========================================

@app.route("/api/mensagem", methods=["POST"])
def receber_mensagem():

    dados = request.get_json()

    mensagem = dados.get("mensagem")

    nome = dados.get(
        "nome",
        "Cliente"
    )

    identificador = dados.get(
        "identificador",
        "teste"
    )

    canal = dados.get(
        "canal",
        "web"
    )


    # Busca ou cria o cliente

    cliente_id = buscar_ou_criar_cliente(
        nome,
        identificador,
        canal
    )


    # Busca o histórico ANTES de salvar
    # a mensagem atual

    historico = buscar_historico(
        cliente_id
    )


    # Salva a mensagem do cliente

    salvar_mensagem(
        cliente_id,
        mensagem,
        "cliente"
    )


    # ==========================================
    # DETECTAR PEDIDO DE ATENDENTE HUMANO
    # ==========================================

    texto = mensagem.lower()

    pedidos_humano = [
        "atendente",
        "humano",
        "falar com alguém",
        "falar com alguem",
        "falar com uma pessoa",
        "atendimento humano"
    ]

    solicitou_humano = any(
        termo in texto
        for termo in pedidos_humano
    )


    if solicitou_humano:

        # Salva uma última resposta automática

        resposta = (
            "Sem problemas! 👤 "
            "Vou encaminhar sua conversa para "
            "um atendente da equipe."
        )

        salvar_mensagem(
            cliente_id,
            resposta,
            "bot"
        )

        # Transfere a conversa para humano

        alterar_modo_atendimento(
            cliente_id,
            "humano"
        )

        return jsonify({
            "cliente_id": cliente_id,
            "mensagem": mensagem,
            "resposta": resposta,
            "modo_atendimento": "humano",
            "transferido": True
        })


    # Descobre quem está responsável
    # pelo atendimento

    modo_atendimento = buscar_modo_atendimento(
        cliente_id
    )

    # ======================================
    # ATENDIMENTO COM IA
    # ======================================

    resposta = processar_mensagem(
        mensagem,
        historico
    )


    # Salva a resposta da IA

    salvar_mensagem(
        cliente_id,
        resposta,
        "bot"
    )


    return jsonify({
        "cliente_id": cliente_id,
        "mensagem": mensagem,
        "resposta": resposta,
        "modo_atendimento": "ia"
    })


# ==========================================
# INICIAR SERVIDOR
# ==========================================

# ==========================================
# RESPOSTA DO ATENDENTE HUMANO
# ==========================================

@app.route(
    "/api/clientes/<int:cliente_id>/responder",
    methods=["POST"]
)
def responder_cliente(cliente_id):

    dados = request.get_json()

    mensagem = dados.get("mensagem")

    if not mensagem:
        return jsonify({
            "erro": "Mensagem não informada"
        }), 400

    modo = buscar_modo_atendimento(cliente_id)

    if modo != "humano":
        return jsonify({
            "erro": "O atendimento ainda está com a IA"
        }), 400

    salvar_mensagem(
        cliente_id,
        mensagem,
        "atendente"
    )

    return jsonify({
        "cliente_id": cliente_id,
        "mensagem": mensagem,
        "remetente": "atendente"
    })

if __name__ == "__main__":
    app.run(debug=True)
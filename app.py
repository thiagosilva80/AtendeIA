from flask import Flask, jsonify, request

from database import (
    criar_tabelas,
    buscar_ou_criar_cliente,
    salvar_mensagem
)

app = Flask(__name__)

criar_tabelas()

@app.route("/")
def home():
    return "AtendeAI está funcionando!"


@app.route("/api/mensagem", methods=["POST"])
def receber_mensagem():

    dados = request.get_json()

    mensagem = dados.get("mensagem")
    nome = dados.get("nome", "Cliente")
    identificador = dados.get("identificador", "teste")
    canal = dados.get("canal", "web")

    cliente_id = buscar_ou_criar_cliente(
        nome,
        identificador,
        canal
    )

    salvar_mensagem(
        cliente_id,
        mensagem,
        "cliente"
    )

    resposta = "Olá! Sou o AtendeAI 👋"

    salvar_mensagem(
        cliente_id,
        resposta,
        "bot"
    )

    return jsonify({
        "cliente_id": cliente_id,
        "mensagem": mensagem,
        "resposta": resposta
    })


if __name__ == "__main__":
    app.run(debug=True)
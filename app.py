from flask import Flask, jsonify, request, render_template
from atendimento import processar_mensagem

from database import (
    criar_tabelas,
    buscar_ou_criar_cliente,
    salvar_mensagem,
    buscar_historico
)

app = Flask(__name__)

criar_tabelas()

@app.route("/")
def home():
    return render_template("index.html")


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

    # Histórico das mensagens anteriores
    historico = buscar_historico(cliente_id)

    # Salva a mensagem atual
    salvar_mensagem(
        cliente_id,
        mensagem,
        "cliente"
    )

    # IA recebe o histórico anterior + mensagem atual
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
        "resposta": resposta
    })

if __name__ == "__main__":
    app.run(debug=True)
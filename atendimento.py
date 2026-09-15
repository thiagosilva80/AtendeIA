from services.ai_service import gerar_resposta_ia


def processar_mensagem(mensagem, historico=None):
    if historico is None:
        historico = []

    resposta = gerar_resposta_ia(
        mensagem,
        historico
    )

    return resposta
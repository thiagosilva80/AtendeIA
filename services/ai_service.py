import os

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def resposta_local(mensagem):

    texto = mensagem.lower()

    if "oi" in texto or "olá" in texto or "ola" in texto:
        return (
            "Olá! 👋 Eu sou o AtendeAI. "
            "Como posso ajudar você?"
        )

    elif "orçamento" in texto or "orcamento" in texto:
        return (
            "Claro! 😊 Posso te ajudar com o orçamento. "
            "Qual serviço você deseja realizar?"
        )

    elif "raspagem" in texto:
        return (
            "Perfeito! Trabalhamos com atendimento para "
            "solicitações de raspagem. Qual é aproximadamente "
            "a metragem do local?"
        )

    elif "humano" in texto or "atendente" in texto:
        return (
            "Claro! Vou registrar que você deseja falar "
            "com um atendente."
        )

    else:
        return (
            "Entendi! 😊 No momento estou funcionando em "
            "modo de desenvolvimento. Pode me contar um "
            "pouco mais sobre o que você precisa?"
        )


def gerar_resposta_ia(mensagem, historico):

    instrucoes = """
    Você é o AtendeAI, um assistente virtual de atendimento empresarial.

    Seu objetivo é:
    - atender clientes com educação;
    - responder de forma clara e objetiva;
    - identificar quando o cliente deseja um orçamento;
    - fazer perguntas para coletar informações importantes;
    - nunca inventar preços;
    - nunca inventar informações sobre a empresa;
    - encaminhar para um atendente humano quando necessário.

    Responda em português brasileiro.
    """

    conversa = []

    for item in historico:

        if item["remetente"] == "cliente":
            role = "user"
        else:
            role = "assistant"

        conversa.append({
            "role": role,
            "content": item["mensagem"]
        })

    conversa.append({
        "role": "user",
        "content": mensagem
    })

    try:

        resposta = client.responses.create(
            model="gpt-5.6-luna",
            instructions=instrucoes,
            input=conversa
        )

        return resposta.output_text

    except RateLimitError:

        print(
            "⚠️ API sem créditos. "
            "Usando modo de desenvolvimento."
        )

        return resposta_local(mensagem)

    except Exception as erro:

        print(
            "⚠️ Erro na API:",
            erro
        )

        return resposta_local(mensagem)
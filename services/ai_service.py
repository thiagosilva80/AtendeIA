import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
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

    resposta = client.responses.create(
        model="gpt-5.6-luna",
        instructions=instrucoes,
        input=conversa
    )

    return resposta.output_text
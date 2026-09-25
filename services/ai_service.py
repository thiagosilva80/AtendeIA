import os

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def resposta_local(mensagem):

    texto = mensagem.lower()

    # PEDIDO PARA FALAR COM HUMANO
    if (
        "atendente" in texto
        or "humano" in texto
        or "falar com alguém" in texto
        or "falar com alguem" in texto
        or "pessoa" in texto
    ):
        return (
            "Sem problemas! 👤 "
            "Vou encaminhar sua conversa para "
            "um atendente da equipe."
        )

    # DEMONSTRAÇÃO
    elif (
        "demonstração" in texto
        or "demonstracao" in texto
    ):
        return (
            "Claro! Podemos registrar seu interesse "
            "em uma demonstração da solução. "
            "Qual é o nome da sua empresa?"
        )

    # SOLUÇÕES PARA EMPRESA
    elif (
        "empresa" in texto
        or "equipe" in texto
        or "soluções" in texto
        or "solucoes" in texto
    ):
        return (
            "Claro! 😊 Temos soluções voltadas para empresas. "
            "Para entender melhor sua necessidade, "
            "quantas pessoas fazem parte da sua equipe?"
        )

    # PLANOS
    elif (
        "plano" in texto
        or "planos" in texto
    ):
        return (
            "Claro! 😊 Posso te ajudar a conhecer "
            "nossas soluções. Você procura uma opção "
            "para uso pessoal ou para sua empresa?"
        )

    # PREÇOS
    elif (
        "preço" in texto
        or "preco" in texto
        or "valor" in texto
    ):
        return (
            "Os valores dependem das necessidades "
            "de cada empresa. Posso coletar algumas "
            "informações para uma solicitação comercial."
        )

    # SAUDAÇÃO
    elif (
        "oi" in texto
        or "olá" in texto
        or "ola" in texto
    ):
        return (
            "Olá! 👋 Eu sou o AtendeAI, "
            "assistente virtual da empresa. "
            "Como posso ajudar você?"
        )

    # RESPOSTA PADRÃO
    else:
        return (
            "Entendi! 😊 Posso fornecer informações "
            "sobre nossos serviços, registrar seu interesse "
            "ou encaminhar você para um atendente."
        )


def gerar_resposta_ia(mensagem, historico):

    instrucoes = """
Você é o AtendeAI, um assistente virtual de atendimento empresarial.

O AtendeAI pode ser utilizado por empresas de diferentes segmentos.

Seu objetivo é:
- receber e atender clientes;
- responder de forma educada, profissional e objetiva;
- entender o que o cliente procura;
- coletar informações importantes;
- identificar oportunidades comerciais;
- registrar interesse em produtos ou serviços;
- nunca inventar preços ou informações;
- manter o contexto da conversa;
- encaminhar o cliente para um atendente humano quando necessário.

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
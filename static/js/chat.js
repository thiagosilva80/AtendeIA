async function enviarMensagem() {
    const input = document.getElementById("mensagem");
    const chat = document.getElementById("chat");

    const mensagem = input.value.trim();

    if (mensagem === "") {
        return;
    }

    const mensagemUsuario = document.createElement("div");

    mensagemUsuario.classList.add(
        "mensagem",
        "usuario"
    );

    mensagemUsuario.textContent = mensagem;

    chat.appendChild(mensagemUsuario);

    input.value = "";

    chat.scrollTop = chat.scrollHeight;

    try {
        const resposta = await fetch(
            "/api/mensagem",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    nome: "Thiago",
                    identificador: "123",
                    canal: "web",
                    mensagem: mensagem
                })
            }
        );

        const dados = await resposta.json();

        const mensagemBot =
            document.createElement("div");

        mensagemBot.classList.add(
            "mensagem",
            "bot"
        );

        mensagemBot.textContent =
            dados.resposta;

        chat.appendChild(mensagemBot);

        chat.scrollTop =
            chat.scrollHeight;
    }

    catch (erro) {
        console.error(
            "Erro ao enviar mensagem:",
            erro
        );
    }
}


document
    .getElementById("mensagem")
    .addEventListener(
        "keypress",
        function(event) {
            if (event.key === "Enter") {
                enviarMensagem();
            }
        }
    );
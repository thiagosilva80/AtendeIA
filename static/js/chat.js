// ==========================================
// CLIENTE ATUALMENTE SELECIONADO
// ==========================================

let clienteSelecionado = null;


// ==========================================
// ENVIAR MENSAGEM
// ==========================================

async function enviarMensagem() {

    const input = document.getElementById("mensagem");
    const chat = document.getElementById("chat");

    const mensagem = input.value.trim();

    if (mensagem === "") {
        return;
    }

    if (!clienteSelecionado) {
        alert("Selecione uma conversa primeiro.");
        return;
    }


    // MOSTRA A MENSAGEM NA TELA

    const mensagemUsuario =
        document.createElement("div");

    mensagemUsuario.classList.add(
        "message",
        "usuario"
    );

    mensagemUsuario.innerHTML = `
        <div class="message-name"></div>
        <div class="bubble"></div>
    `;

    mensagemUsuario
        .querySelector(".message-name")
        .textContent = clienteSelecionado.nome;

    mensagemUsuario
        .querySelector(".bubble")
        .textContent = mensagem;

    chat.appendChild(mensagemUsuario);

    input.value = "";

    chat.scrollTop = chat.scrollHeight;

    // ==========================================
// MODO HUMANO
// ==========================================

if (
    clienteSelecionado.modo_atendimento
    === "humano"
) {

    try {

        const resposta = await fetch(
            `/api/clientes/${clienteSelecionado.id}/responder`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    mensagem: mensagem
                })
            }
        );

        const dados = await resposta.json();

        if (!resposta.ok) {
            alert(dados.erro);
            return;
        }

        // Recarrega a conversa para mostrar
        // a mensagem salva no banco

        await carregarConversa(
            clienteSelecionado.id,
            clienteSelecionado.nome,
            clienteSelecionado.canal
        );

        carregarClientes();

        return;

    }

    catch (erro) {

        console.error(
            "Erro ao responder cliente:",
            erro
        );

        return;
    }
}


    try {

        const resposta = await fetch(
            "/api/mensagem",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    nome: clienteSelecionado.nome,

                    identificador:
                        clienteSelecionado.identificador,

                    canal:
                        clienteSelecionado.canal,

                    mensagem: mensagem

                })
            }
        );


        const dados = await resposta.json();
    
                // ==========================================
        // ATUALIZA MODO IA / HUMANO
        // ==========================================

        if (dados.modo_atendimento) {

            clienteSelecionado.modo_atendimento =
                dados.modo_atendimento;

            atualizarModoAtendimento();

        }

        // RESPOSTA DO ATENDEAI

        if (dados.resposta) {

            const mensagemBot =
                document.createElement("div");

            mensagemBot.classList.add(
                "message",
                "bot"
            );

            mensagemBot.innerHTML = `
                <div class="message-name">
                    🤖 AtendeAI
                </div>

                <div class="bubble"></div>
            `;

            mensagemBot
                .querySelector(".bubble")
                .textContent = dados.resposta;

            chat.appendChild(mensagemBot);

        }


        chat.scrollTop = chat.scrollHeight;

        carregarClientes();

    }

    catch (erro) {

        console.error(
            "Erro ao enviar mensagem:",
            erro
        );

    }
}


// ==========================================
// ENTER PARA ENVIAR
// ==========================================

document
    .getElementById("mensagem")
    .addEventListener(
        "keydown",
        function(event) {

            if (event.key === "Enter") {
                enviarMensagem();
            }

        }
    );


// ==========================================
// CARREGAR CLIENTES
// ==========================================

async function carregarClientes() {

    try {

        const resposta =
            await fetch("/api/clientes");

        const clientes =
            await resposta.json();

        const lista =
            document.getElementById(
                "lista-conversas"
            );

        lista.innerHTML = "";


        clientes.forEach(cliente => {

            const conversa =
                document.createElement("div");

            conversa.classList.add(
                "conversation"
            );


            // DESTACA O CLIENTE SELECIONADO

            if (
                clienteSelecionado &&
                clienteSelecionado.id === cliente.id
            ) {

                conversa.classList.add("active");

            }


            const inicial =
                cliente.nome
                    ? cliente.nome
                        .charAt(0)
                        .toUpperCase()
                    : "?";


            const ultimaMensagem =
                cliente.ultima_mensagem ||
                "Nenhuma mensagem";


            conversa.innerHTML = `
                <div class="avatar">
                    ${inicial}
                </div>

                <div class="conversation-info">

                    <strong>
                        ${cliente.nome}
                    </strong>

                    <span>
                        ${ultimaMensagem}
                    </span>

                </div>

                <div class="status-dot"></div>
            `;


            // CLIQUE NA CONVERSA

            conversa.addEventListener(
                "click",
                function() {

                    clienteSelecionado = cliente;

                    carregarConversa(
                        cliente.id,
                        cliente.nome,
                        cliente.canal
                    );

                    carregarClientes();

                }
            );


            lista.appendChild(conversa);

        });

    }

    catch (erro) {

        console.error(
            "Erro ao carregar clientes:",
            erro
        );

    }

}


// ==========================================
// CARREGAR HISTÓRICO
// ==========================================

async function carregarConversa(
    clienteId,
    nome,
    canal
) {

    try {

        const resposta = await fetch(
            `/api/clientes/${clienteId}/mensagens`
        );

        const mensagens =
            await resposta.json();

        const chat =
            document.getElementById("chat");


        // ==========================================
        // ATUALIZAR DADOS DO CLIENTE
        // ==========================================

        document
            .getElementById("chat-cliente-nome")
            .textContent = nome;


        document
            .getElementById("cliente-nome")
            .textContent = nome;


        // AVATAR

        const inicial =
            nome
                ? nome.charAt(0).toUpperCase()
                : "?";

        document
            .getElementById("cliente-avatar")
            .textContent = inicial;


        // CANAL

        const elementoCanal =
            document.getElementById(
                "cliente-canal"
            );

        if (canal === "whatsapp") {

            elementoCanal.textContent =
                "💬 WhatsApp";

        }

        else if (canal === "telegram") {

            elementoCanal.textContent =
                "✈️ Telegram";

        }

        else {

            elementoCanal.textContent =
                "🌐 Web Chat";

        }


        // ATUALIZA IA / HUMANO

        atualizarModoAtendimento();


        // LIMPA O CHAT

        chat.innerHTML = "";


        // ==========================================
        // CARREGAR MENSAGENS
        // ==========================================

        mensagens.forEach(item => {

            const elemento =
                document.createElement("div");


            // ======================================
            // MENSAGEM DO CLIENTE
            // ======================================

            if (item.remetente === "cliente") {

                elemento.classList.add(
                    "message",
                    "usuario"
                );

                elemento.innerHTML = `
                    <div class="message-name"></div>

                    <div class="bubble"></div>
                `;

                elemento
                    .querySelector(".message-name")
                    .textContent = nome;

            }


            // ======================================
            // MENSAGEM DO ATENDENTE
            // ======================================

            else if (
                item.remetente === "atendente"
            ) {

                elemento.classList.add(
                    "message",
                    "bot"
                );

                elemento.innerHTML = `
                    <div class="message-name">
                        👤 Atendente
                    </div>

                    <div class="bubble"></div>
                `;

            }


            // ======================================
            // MENSAGEM DA IA
            // ======================================

            else {

                elemento.classList.add(
                    "message",
                    "bot"
                );

                elemento.innerHTML = `
                    <div class="message-name">
                        🤖 AtendeAI
                    </div>

                    <div class="bubble"></div>
                `;

            }


            elemento
                .querySelector(".bubble")
                .textContent = item.mensagem;


            chat.appendChild(elemento);

        });


        // DESCE PARA A ÚLTIMA MENSAGEM

        chat.scrollTop =
            chat.scrollHeight;

    }

    catch (erro) {

        console.error(
            "Erro ao carregar conversa:",
            erro
        );

    }

}

// ==========================================
// ALTERNAR IA / HUMANO
// ==========================================

async function alternarAtendimento() {

    if (!clienteSelecionado) {

        alert("Selecione uma conversa primeiro.");

        return;

    }


    const modoAtual =
        clienteSelecionado.modo_atendimento;


    const novoModo =
        modoAtual === "ia"
            ? "humano"
            : "ia";


    try {

        const resposta = await fetch(
            `/api/clientes/${clienteSelecionado.id}/modo`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    modo: novoModo
                })
            }
        );


        const dados = await resposta.json();


        clienteSelecionado.modo_atendimento =
            dados.modo;


        atualizarModoAtendimento();

        carregarClientes();

    }

    catch (erro) {

        console.error(
            "Erro ao alterar atendimento:",
            erro
        );

    }

}


// ==========================================
// ATUALIZAR PAINEL IA / HUMANO
// ==========================================

function atualizarModoAtendimento() {

    if (!clienteSelecionado) {
        return;
    }

    const textoModo =
        document.getElementById(
            "modo-atendimento"
        );

    const botao =
        document.getElementById(
            "btn-assumir"
        );

    const statusTopo =
        document.getElementById(
            "chat-status-ia"
        );

    const input =
        document.getElementById(
            "mensagem"
        );


    if (!textoModo || !botao) {

        console.error(
            "Elementos do modo de atendimento não encontrados."
        );

        return;
    }


    // ==========================================
    // ATENDIMENTO HUMANO
    // ==========================================

    if (
        clienteSelecionado.modo_atendimento
        === "humano"
    ) {

        textoModo.textContent =
            "👤 Atendimento humano";

        botao.textContent =
            "✨ Devolver para IA";

        if (statusTopo) {
            statusTopo.textContent =
                "👤 Humano";
        }

        if (input) {
            input.placeholder =
                "Responder como atendente...";
        }

    }


    // ==========================================
    // ATENDIMENTO COM IA
    // ==========================================

    else {

        textoModo.textContent =
            "✨ Inteligência Artificial";

        botao.textContent =
            "👤 Assumir atendimento";

        if (statusTopo) {
            statusTopo.textContent =
                "✨ IA";
        }

        if (input) {
            input.placeholder =
                "Simular mensagem do cliente...";
        }

    }

}


// ==========================================
// INICIAR DASHBOARD
// ==========================================

carregarClientes();
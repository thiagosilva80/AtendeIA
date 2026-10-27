# AtendeIA

# 🤖 AtendeAI

Sistema de atendimento empresarial desenvolvido com Python e Flask, criado para centralizar conversas, automatizar respostas e permitir a transferência entre Inteligência Artificial e atendimento humano.

O projeto foi desenvolvido como parte dos meus estudos em Análise e Desenvolvimento de Sistemas e faz parte do meu portfólio profissional.

---

## 📌 Sobre o projeto

O AtendeAI é uma aplicação web que simula uma plataforma de atendimento ao cliente.

A proposta é permitir que empresas possam organizar conversas em um único painel, utilizar IA para o atendimento inicial e transferir a conversa para um atendente humano quando necessário.

O sistema foi desenvolvido pensando em uma arquitetura que futuramente poderá receber mensagens de diferentes canais.

---

## ✨ Funcionalidades

- 💬 Sistema de conversas
- 👥 Gerenciamento de clientes
- 🗂️ Histórico de mensagens
- 🤖 Atendimento automatizado
- 👤 Atendimento humano
- 🔄 Alternância entre IA e atendente
- 🚨 Transferência para humano quando solicitada pelo cliente
- 💾 Persistência das conversas no banco de dados
- 🔌 API desenvolvida com Flask
- 🖥️ Dashboard de atendimento
- 📱 Interface responsiva

---

## 🛠️ Tecnologias utilizadas

### Backend

- Python
- Flask

### Banco de dados

- SQLite

### Frontend

- HTML5
- CSS3
- JavaScript

### Outras tecnologias e conceitos

- APIs REST
- JSON
- Git
- GitHub
- Integração com Inteligência Artificial
- Manipulação de banco de dados
- Arquitetura cliente-servidor

---

## 🧠 Como funciona

O fluxo básico do sistema é:

Cliente
↓
API Flask
↓
Identificação do cliente
↓
Histórico da conversa
↓
Modo de atendimento
↓
IA ou Atendente Humano
↓
Banco de dados
↓
Dashboard

Quando uma nova mensagem é recebida, o sistema identifica o cliente e registra a mensagem no banco de dados.

Se o atendimento estiver no modo IA, o sistema gera uma resposta automaticamente.

Caso o cliente solicite atendimento humano, a conversa é transferida e o atendente pode continuar o atendimento através do dashboard.

---

## 👤 Atendimento humano

Uma das funcionalidades do projeto é a possibilidade de alternar entre:

🤖 Inteligência Artificial

e

👤 Atendimento Humano

O atendente consegue assumir uma conversa e posteriormente devolver o atendimento para a IA.

---

## 📂 Estrutura do projeto

AtendeIA/

├── app.py
├── database.py
├── atendimento.py
│
├── services/
│   └── ai_service.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── chat.js
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md

---

## ▶️ Como executar o projeto

### 1. Clone o repositório

git clone URL_DO_SEU_REPOSITORIO

### 2. Entre na pasta

cd AtendeIA

### 3. Crie um ambiente virtual

python -m venv venv

### 4. Ative o ambiente virtual

Windows:

venv\Scripts\activate

### 5. Instale as dependências

pip install -r requirements.txt

### 6. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto.

As chaves e credenciais utilizadas pelo sistema não devem ser publicadas no GitHub.

### 7. Execute o projeto

python app.py

A aplicação estará disponível normalmente em:

http://127.0.0.1:5000

---

## 🔐 Segurança

Informações sensíveis não são armazenadas diretamente no código.

O arquivo `.env` é utilizado para variáveis de ambiente e deve permanecer fora do repositório através do `.gitignore`.

Exemplo:

.env
venv/
__pycache__/
*.db

---

## 🚧 Próximas melhorias

- 📲 Integração com WhatsApp
- ✈️ Integração com Telegram
- 🌐 Chat web para clientes
- ⚡ Atualização das conversas em tempo real
- 🔔 Notificações para novos atendimentos
- 📊 Métricas de atendimento
- 🔎 Busca de clientes e conversas
- 👥 Sistema de usuários para atendentes
- 🔐 Autenticação
- ☁️ Deploy da aplicação

---

## 🎯 Objetivo

O principal objetivo deste projeto é colocar em prática conhecimentos de desenvolvimento backend, banco de dados, APIs e desenvolvimento web através da criação de uma aplicação próxima de um cenário empresarial real.

Além disso, o projeto está sendo desenvolvido continuamente como parte do meu portfólio para oportunidades na área de tecnologia.

---

## 👨‍💻 Autor

**Thiago Matheus**

Estudante de Análise e Desenvolvimento de Sistemas.

Em busca de oportunidades de estágio na área de tecnologia.

---

⭐ Se você gostou do projeto, considere deixar uma estrela no repositório!

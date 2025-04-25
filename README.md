# Zer0Bot - O Bot da Legião Brasileira 🇧🇷

Um bot completo e open-source para comunidades do Discord, com foco em jogos como Supremacy 1914 e recursos avançados de moderação, interação e automação.

> Desenvolvido com 💚 por [TheuZer0] e para a comunidade da [LBRA – Legião Brasileira](https://discord.gg/UMy27sqzXK)

---

## ✨ Funcionalidades

- ✅ Moderação (ban, kick, mute, warn)
- ✅ AutoMod (anti-flood, anti-spam, anti-link)
- ✅ Sistema de níveis e XP por atividade
- ✅ Auto-roles e boas-vindas
- ✅ Reaction roles
- ✅ Logs de mensagens, punições e ações administrativas
- ✅ Comandos customizáveis
- ✅ Sorteios e concursos automatizados
- ✅ Comandos de diversão (piadas, memes, gifs)
- ✅ Feed automático do Supremacy 1914
- ✅ Estatísticas de servidor e ranking de atividade
- ✅ Sistema de convites e recrutamento
- ✅ Painel web leve (futuramente)
- E muito mais!

---

## ⚙️ Tecnologias usadas

- Python 3.10+
- [discord.py](https://github.com/Rapptz/discord.py)
- SQLite (ou PostgreSQL/MongoDB em produção)
- `.env` para variáveis sensíveis
- JSON/Storage local temporário
- Organização modular via `cogs`

---

## Documentação

- [Planejamento](docs/Planejamento.md)

---

### Criando o Bot no Discord

1. Acesse [https://discord.com/developers/applications](https://discord.com/developers/applications)
2. Clique em **“New Application”** e dê o nome de **Zer0Bot**
3. Vá até a aba **“Bot”**, clique em **“Add Bot”** e confirme
4. Em **Token**, clique em **“Reset Token”** e copie o token para usar no `.env`
5. Ative as **Intents**:
   - `MESSAGE CONTENT INTENT`
   - `PRESENCE INTENT`
   - `SERVER MEMBERS INTENT`
6. Vá na aba **OAuth2 > URL Generator** e marque:
   - **Scopes**: `bot`, `applications.commands`
   - **Bot Permissions**: marque tudo que o Zer0Bot vai precisar, como:
     - `Manage Roles`, `Manage Messages`, `Send Messages`, `Read Message History`, `Kick Members`, etc.
7. Copie o link gerado e cole no navegador para adicionar o bot ao seu servidor

## 🚀 Como rodar localmente

### 1. Clone o repositório
```bash
git clone https://github.com/Zer0G0ld/Zer0.git
cd Zer0
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Crie um arquivo `.env` com:
```
DISCORD_TOKEN=seu_token_aqui
PREFIX=!
OWNER_ID=seu_id_aqui
```

### 5. Inicie o bot
```bash
python bot.py
```

---

## 📁 Estrutura do Projeto

```
Zer0Bot/
│
├── cogs/                 # Comandos organizados por módulo
│   ├── moderação.py
│   ├── xp.py
│   ├── diversão.py
│   └── ...
│
├── data/                 # JSONs, banco de dados, configs
│
├── utils/                # Funções auxiliares
│
├── bot.py                # Arquivo principal
├── requirements.txt      # Dependências
└── .env                  # Variáveis de ambiente (não subir pro Git)
```

---

## 🧠 Contribuindo

- Fork o repositório
- Crie uma branch: `git checkout -b minha-feature`
- Faça seu commit: `git commit -m "Nova funcionalidade"`
- Envie seu PR 🙌

---

## 📜 Licença

Este projeto é open-source sob a [LICENÇA](LICENSE). Faça o que quiser, só não tire os créditos 😎

---

## 🤝 Entre na comunidade

Junte-se à [Legião Brasileira – LBRA](https://discord.gg/UMy27sqzXK) e jogue com a elite estratégica do Brasil!

---

Vitória ou morte. LBRA no topo.  

---
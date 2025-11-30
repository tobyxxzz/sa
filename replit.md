# Bot do Discord

## Overview
Dois bots do Discord configurados para rodar simultaneamente no Replit:
1. **Bot de Tickets** - Sistema automático de suporte com respostas a palavras-chave
2. **Bot de Staff** - Comandos de moderação para gerenciamento do servidor

**Current State:** Ambos os bots rodando com uptime monitoring via Flask
**Last Updated:** November 30, 2025

## Project Architecture

### Structure
- `main.py` - Arquivo principal que gerencia ambos os bots em threads separadas
- `bot_tickets.py` - Bot de Tickets com comandos de suporte
- `bot_staff.py` - Bot de Staff com comandos de moderação
- `requirements.txt` - Dependências Python (discord.py, flask)
- `.replit` - Configuração do Replit
- `.gitignore` - Padrões de arquivos ignorados

### Technology Stack
- **Language:** Python 3.11
- **Libraries:** discord.py 2.6.4+, Flask
- **Environment:** Replit (NixOS-based)
- **Web Server:** Flask (uptime monitoring na porta 8080)

## Funcionalidades

### Bot de Tickets
#### Sistema de Tickets Automático
Quando alguém manda uma mensagem em canais com "ticket" no nome:
- Bot envia mensagem de boas-vindas automática (apenas uma vez por usuário por canal)
- Explica os comandos disponíveis
- Ignora mensagens de outros bots

#### Comandos de Texto Simples (sem prefixo)
- **script** - Envia o script do Roblox automaticamente
- **aura** - Envia os links dos 3 game passes de aura
- **discord** - Envia o link do servidor Discord
- **suporte** - Marca @ADM e registra pedido de suporte

#### Slash Commands (/)
- `/ping` - Mostra a latência do bot
- `/script` - Script do Roblox
- `/aura` - Links das auras
- `/discord` - Link do Discord
- `/suporte` - Pedir suporte com @ADM
- `/ajuda` - Mostra lista de comandos

#### Comandos com Prefixo (!)
- `!ping` - Mostra a latência do bot
- `!oi` - Bot responde com saudação
- `!ajuda` - Mostra lista de comandos

### Bot de Staff
#### Slash Commands (/) de Moderação
- `/ban @membro [motivo]` - Banir um membro do servidor
- `/mute @membro [motivo]` - Silenciar um membro (cria role "Silenciado")
- `/unmute @membro` - Dessilenciar um membro
- `/lock [#canal]` - Trancar um canal (padrão: canal atual)
- `/unlock [#canal]` - Destrancar um canal (padrão: canal atual)
- `/ajuda_staff` - Mostra lista de comandos de staff

#### Comandos com Prefixo (!)
- `!ban @membro [motivo]` - Banir um membro do servidor
- `!mute @membro [motivo]` - Silenciar um membro (cria role "Silenciado")
- `!unmute @membro` - Dessilenciar um membro
- `!lock [#canal]` - Trancar um canal (padrão: canal atual)
- `!unlock [#canal]` - Destrancar um canal (padrão: canal atual)
- `!ajuda_staff` - Mostra lista de comandos de staff

Todos os comandos verificam permissões antes de executar.

### Web Server (Uptime Monitoring)
- Flask roda na porta 8080
- Endpoint `/` retorna "Bots online 😎"
- Permite integração com serviços de monitoramento (UptimeRobot, etc)

## Configuração

### Tokens do Discord

Ambos os bots precisam de tokens armazenados nas Secrets do Replit:

1. **DISCORD_BOT_TOKEN** - Token do Bot de Tickets
2. **DISCORD_STAFF_BOT_TOKEN** - Token do Bot de Staff

**Como obter os tokens:**
1. Acesse https://discord.com/developers/applications
2. Crie uma nova aplicação ou selecione uma existente
3. Vá em "Bot" no menu lateral
4. Clique em "Reset Token" ou "Copy" para obter o token
5. Adicione o token nas Secrets do Replit

### Intents Necessários

Os bots usam os seguintes intents:
- `message_content` - Para ler conteúdo de mensagens
- `members` - Para acessar informações de membros
- `guilds` - Para gerenciar guildas
- Default intents

**Ative esses intents no Discord Developer Portal:**
1. Vá em Bot > Privileged Gateway Intents
2. Ative "MESSAGE CONTENT INTENT"
3. Ative "SERVER MEMBERS INTENT"

### Permissões do Discord

**Bot de Tickets precisa de:**
- Send Messages
- Read Messages/View Channels
- Mention @everyone, @here, and All Roles

**Bot de Staff precisa de:**
- Send Messages
- Read Messages/View Channels
- Ban Members
- Manage Messages
- Manage Channels
- Mention @everyone, @here, and All Roles

## Rodando os Bots

Os bots rodam automaticamente via workflow "Run Bot". Para ver o status:
- Verifique os logs do console
- Você verá "Bot de Tickets está online e pronto!" e "Bot de Staff está online e pronto!" quando conectarem
- Flask server roda em paralelo para uptime monitoring

## Recent Changes

### November 30, 2025 - Slash Commands e Separação de Bots
- Refatorado código em arquivos separados (bot_tickets.py e bot_staff.py)
- Adicionados slash commands (/) para todos os comandos
- Melhorada organização do código
- Ambos os bots rodando simultaneamente em threads separadas

### November 30, 2025 - Implementação do Bot de Staff
- Criado bot de staff com comandos de moderação (ban, mute, unmute, lock, unlock)
- Ambos os bots agora rodam simultaneamente em threads separadas
- Flask web server mantém os bots vivos e permite uptime monitoring
- Adicionado tratamento de erros nos comandos de staff
- Sistema rastreia estado de membros silenciados e canais trancados

## User Preferences
- Idioma: Português (BR)
- Uptime monitoring: Sim (Flask server)
- Formato de comandos: Slash commands (/)

# Guia de Configuração dos Bots

## Passo 1: Criar os Bots no Discord Developer Portal

### Para o Bot de Tickets:
1. Acesse https://discord.com/developers/applications
2. Clique em "New Application" e nomeie como "Bot de Tickets"
3. Vá para a aba "Bot" no menu lateral
4. Clique em "Add Bot"
5. Sob a seção "TOKEN", clique em "Copy" para copiar o token
6. Adicione este token nas Secrets do Replit com a chave: `DISCORD_BOT_TOKEN`

### Para o Bot de Staff:
1. No Discord Developer Portal, clique em "New Application" e nomeie como "Bot de Staff"
2. Vá para a aba "Bot"
3. Clique em "Add Bot"
4. Copie o token
5. Adicione este token nas Secrets do Replit com a chave: `DISCORD_STAFF_BOT_TOKEN`

## Passo 2: Ativar Intents Necessários

Para CADA bot que você criou, faça isso:

1. No Discord Developer Portal, vá para **Bot > Privileged Gateway Intents**
2. Ative os seguintes intents:
   - ✅ **PRESENCE INTENT** (opcional, para status do bot)
   - ✅ **SERVER MEMBERS INTENT** (obrigatório - para comandos de moderação)
   - ✅ **MESSAGE CONTENT INTENT** (obrigatório - para ler mensagens)

3. Clique em "Save Changes"

## Passo 3: Adicionar Permissões do Bot

### Para o Bot de Tickets:
1. Na aba "Bot", procure por **"Scopes"** ou use o URL Generator
2. Selecione escopos: `bot`
3. Selecione permissões:
   - ✅ Send Messages
   - ✅ Read Messages/View Channels
   - ✅ Mention @everyone, @here, and All Roles

4. Copie a URL gerada e abra em seu navegador para adicionar o bot ao servidor

### Para o Bot de Staff:
1. Selecione escopos: `bot`
2. Selecione permissões:
   - ✅ Send Messages
   - ✅ Read Messages/View Channels
   - ✅ Ban Members
   - ✅ Manage Messages
   - ✅ Manage Channels
   - ✅ Mention @everyone, @here, and All Roles

3. Copie a URL gerada e abra em seu navegador para adicionar o bot ao servidor

## Passo 4: Adicionar Tokens às Secrets do Replit

1. No seu projeto Replit, clique em "Secrets" (ícone de chave)
2. Adicione:
   - **Key:** `DISCORD_BOT_TOKEN` | **Value:** [token do bot de tickets]
   - **Key:** `DISCORD_STAFF_BOT_TOKEN` | **Value:** [token do bot de staff]
3. Clique em "Add Secret" para cada um

## Passo 5: Rodar os Bots

Os bots iniciarão automaticamente. Você verá nos logs:
- "Bot de Tickets está online e pronto!"
- "Bot de Staff está online e pronto!"

Se receber erros sobre intents, certifique-se de ter ativado todos os intents no passo 2.

## Testando os Bots

### Bot de Tickets:
- Em um canal com "ticket" no nome, digite: `script`, `aura`, `discord`, ou `suporte`
- Use comandos: `!ping`, `!oi`, `!ajuda`

### Bot de Staff:
- Use comandos de moderação: `!ban @usuario motivo`, `!mute @usuario`, `!unmute @usuario`
- Use `!lock` e `!unlock` para gerenciar canais
- Use `!ajuda_staff` para ver todos os comandos

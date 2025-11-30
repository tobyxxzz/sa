import discord
from discord.ext import commands
from datetime import timedelta

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot_staff = commands.Bot(command_prefix='!', intents=intents)

# ID do servidor autorizado
SERVIDOR_ID = 1437020610269155431

timeout_options = {
    "60s": timedelta(seconds=60),
    "5m": timedelta(minutes=5),
    "10m": timedelta(minutes=10),
    "1h": timedelta(hours=1),
    "1d": timedelta(days=1),
    "1w": timedelta(weeks=1),
}

durations = ["60s", "5m", "10m", "1h", "1d", "1w"]

@bot_staff.event
async def on_ready():
    print(f'Bot de Staff conectado como {bot_staff.user.name} (ID: {bot_staff.user.id})')
    print('------')
    print('Bot de Staff está online e pronto!')
    try:
        synced = await bot_staff.tree.sync()
        print(f"Sincronizados {len(synced)} comandos de Staff")
    except Exception as e:
        print(f"Erro ao sincronizar comandos de Staff: {e}")

@bot_staff.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="Membro Banido",
            description=f"{member.mention} foi banido do servidor",
            color=discord.Color.red()
        )
        if reason:
            embed.add_field(name="Motivo", value=reason, inline=False)
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("❌ Não tenho permissão para banir este membro!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao banir: {str(e)}")

@bot_staff.command(name='mute')
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, duration: str = "5m", *, reason=None):
    try:
        if duration not in timeout_options:
            await ctx.send("❌ Duração inválida! Use: 60s, 5m, 10m, 1h, 1d, 1w")
            return
        
        timeout_duration = timeout_options[duration]
        await member.timeout(timeout_duration, reason=reason)
        
        embed = discord.Embed(
            title="Membro Silenciado (Timeout)",
            description=f"{member.mention} foi silenciado por {duration}",
            color=discord.Color.orange()
        )
        if reason:
            embed.add_field(name="Motivo", value=reason, inline=False)
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("❌ Não tenho permissão para dar timeout neste membro!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao dar timeout: {str(e)}")

@bot_staff.command(name='unmute')
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    try:
        await member.timeout(None)
        embed = discord.Embed(
            title="Membro Dessilenciado",
            description=f"{member.mention} foi dessilenciado",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("❌ Não tenho permissão para remover timeout deste membro!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao remover timeout: {str(e)}")

@bot_staff.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="Membro Expulso",
            description=f"{member.mention} foi expulso do servidor",
            color=discord.Color.gold()
        )
        if reason:
            embed.add_field(name="Motivo", value=reason, inline=False)
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("❌ Não tenho permissão para expulsar este membro!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao expulsar: {str(e)}")

@bot_staff.command(name='lock')
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: discord.TextChannel = None):
    if channel is None:
        channel = ctx.channel
    
    try:
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed = discord.Embed(
            title="Canal Trancado",
            description=f"{channel.mention} foi trancado",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("❌ Não tenho permissão para trancar este canal!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao trancar: {str(e)}")

@bot_staff.command(name='unlock')
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: discord.TextChannel = None):
    if channel is None:
        channel = ctx.channel
    
    try:
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        embed = discord.Embed(
            title="Canal Destancado",
            description=f"{channel.mention} foi destrancado",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("❌ Não tenho permissão para destrancar este canal!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao destrancar: {str(e)}")

@bot_staff.tree.command(name="ban", description="Banir um membro do servidor")
@discord.app_commands.describe(membro="Membro a ser banido", motivo="Motivo do ban (opcional)")
async def slash_ban(interaction: discord.Interaction, membro: discord.Member, motivo: str = None):
    if interaction.guild_id != SERVIDOR_ID:
        await interaction.response.send_message("❌ Este comando só pode ser usado no servidor autorizado!")
        return
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("❌ Você não tem permissão para usar este comando!")
        return
    try:
        await membro.ban(reason=motivo)
        embed = discord.Embed(
            title="Membro Banido",
            description=f"{membro.mention} foi banido do servidor",
            color=discord.Color.red()
        )
        if motivo:
            embed.add_field(name="Motivo", value=motivo, inline=False)
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Não tenho permissão para banir este membro!")
    except Exception as e:
        await interaction.response.send_message(f"❌ Erro ao banir: {str(e)}")

@bot_staff.tree.command(name="mute", description="Silenciar um membro com timeout")
@discord.app_commands.describe(
    membro="Membro a ser silenciado",
    duracao="Duração: 60s, 5m, 10m, 1h, 1d, 1w"
)
@discord.app_commands.choices(duracao=[
    discord.app_commands.Choice(name="60 segundos", value="60s"),
    discord.app_commands.Choice(name="5 minutos", value="5m"),
    discord.app_commands.Choice(name="10 minutos", value="10m"),
    discord.app_commands.Choice(name="1 hora", value="1h"),
    discord.app_commands.Choice(name="1 dia", value="1d"),
    discord.app_commands.Choice(name="1 semana", value="1w"),
])
async def slash_mute(interaction: discord.Interaction, membro: discord.Member, duracao: str, motivo: str = None):
    if interaction.guild_id != SERVIDOR_ID:
        await interaction.response.send_message("❌ Este comando só pode ser usado no servidor autorizado!")
        return
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("❌ Você não tem permissão para usar este comando!")
        return
    
    try:
        timeout_duration = timeout_options[duracao]
        await membro.timeout(timeout_duration, reason=motivo)
        embed = discord.Embed(
            title="Membro Silenciado (Timeout)",
            description=f"{membro.mention} foi silenciado por {duracao}",
            color=discord.Color.orange()
        )
        if motivo:
            embed.add_field(name="Motivo", value=motivo, inline=False)
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Não tenho permissão para dar timeout neste membro!")
    except Exception as e:
        await interaction.response.send_message(f"❌ Erro ao dar timeout: {str(e)}")

@bot_staff.tree.command(name="unmute", description="Remover timeout de um membro")
@discord.app_commands.describe(membro="Membro a ser dessilenciado")
async def slash_unmute(interaction: discord.Interaction, membro: discord.Member):
    if interaction.guild_id != SERVIDOR_ID:
        await interaction.response.send_message("❌ Este comando só pode ser usado no servidor autorizado!")
        return
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("❌ Você não tem permissão para usar este comando!")
        return
    try:
        await membro.timeout(None)
        embed = discord.Embed(
            title="Membro Dessilenciado",
            description=f"{membro.mention} foi dessilenciado",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Não tenho permissão para remover timeout deste membro!")
    except Exception as e:
        await interaction.response.send_message(f"❌ Erro ao remover timeout: {str(e)}")

@bot_staff.tree.command(name="kick", description="Expulsar um membro do servidor")
@discord.app_commands.describe(membro="Membro a ser expulso", motivo="Motivo do kick (opcional)")
async def slash_kick(interaction: discord.Interaction, membro: discord.Member, motivo: str = None):
    if interaction.guild_id != SERVIDOR_ID:
        await interaction.response.send_message("❌ Este comando só pode ser usado no servidor autorizado!")
        return
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("❌ Você não tem permissão para usar este comando!")
        return
    try:
        await membro.kick(reason=motivo)
        embed = discord.Embed(
            title="Membro Expulso",
            description=f"{membro.mention} foi expulso do servidor",
            color=discord.Color.gold()
        )
        if motivo:
            embed.add_field(name="Motivo", value=motivo, inline=False)
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Não tenho permissão para expulsar este membro!")
    except Exception as e:
        await interaction.response.send_message(f"❌ Erro ao expulsar: {str(e)}")

@bot_staff.tree.command(name="lock", description="Trancar um canal")
@discord.app_commands.describe(canal="Canal a ser trancado (deixe em branco para o canal atual)")
async def slash_lock(interaction: discord.Interaction, canal: discord.TextChannel = None):
    if interaction.guild_id != SERVIDOR_ID:
        await interaction.response.send_message("❌ Este comando só pode ser usado no servidor autorizado!")
        return
    if not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message("❌ Você não tem permissão para usar este comando!")
        return
    if canal is None:
        canal = interaction.channel
    
    try:
        await canal.set_permissions(interaction.guild.default_role, send_messages=False)
        embed = discord.Embed(
            title="Canal Trancado",
            description=f"{canal.mention} foi trancado",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Não tenho permissão para trancar este canal!")
    except Exception as e:
        await interaction.response.send_message(f"❌ Erro ao trancar: {str(e)}")

@bot_staff.tree.command(name="unlock", description="Destrancar um canal")
@discord.app_commands.describe(canal="Canal a ser destrancado (deixe em branco para o canal atual)")
async def slash_unlock(interaction: discord.Interaction, canal: discord.TextChannel = None):
    if interaction.guild_id != SERVIDOR_ID:
        await interaction.response.send_message("❌ Este comando só pode ser usado no servidor autorizado!")
        return
    if not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message("❌ Você não tem permissão para usar este comando!")
        return
    if canal is None:
        canal = interaction.channel
    
    try:
        await canal.set_permissions(interaction.guild.default_role, send_messages=True)
        embed = discord.Embed(
            title="Canal Destrancado",
            description=f"{canal.mention} foi destrancado",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Não tenho permissão para destrancar este canal!")
    except Exception as e:
        await interaction.response.send_message(f"❌ Erro ao destrancar: {str(e)}")

@bot_staff.tree.command(name="dar_cargo", description="Dar um cargo a um membro")
@discord.app_commands.describe(membro="Membro que receberá o cargo", cargo="Cargo a ser atribuído")
async def slash_dar_cargo(interaction: discord.Interaction, membro: discord.Member, cargo: discord.Role):
    if interaction.guild_id != SERVIDOR_ID:
        await interaction.response.send_message("❌ Este comando só pode ser usado no servidor autorizado!")
        return
    # Verificar se o usuário tem permissão manage_roles ou é admin
    if not (interaction.user.guild_permissions.manage_roles or interaction.user.guild_permissions.administrator):
        await interaction.response.send_message("❌ Você não tem permissão para usar este comando!")
        return
    
    # Verificar hierarquia de cargos
    if cargo >= interaction.user.top_role:
        await interaction.response.send_message("❌ Você só pode atribuir cargos menores que o seu cargo mais alto!")
        return
    
    try:
        await membro.add_roles(cargo)
        embed = discord.Embed(
            title="Cargo Atribuído",
            description=f"{membro.mention} recebeu o cargo {cargo.mention}",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Não tenho permissão para atribuir este cargo! Verifique se meu cargo está acima do cargo a ser atribuído.")
    except Exception as e:
        await interaction.response.send_message(f"❌ Erro ao atribuir cargo: {str(e)}")

@bot_staff.tree.command(name="remover_cargo", description="Remover um cargo de um membro")
@discord.app_commands.describe(membro="Membro que terá o cargo removido", cargo="Cargo a ser removido")
async def slash_remover_cargo(interaction: discord.Interaction, membro: discord.Member, cargo: discord.Role):
    if interaction.guild_id != SERVIDOR_ID:
        await interaction.response.send_message("❌ Este comando só pode ser usado no servidor autorizado!")
        return
    # Verificar se o usuário tem permissão manage_roles ou é admin
    if not (interaction.user.guild_permissions.manage_roles or interaction.user.guild_permissions.administrator):
        await interaction.response.send_message("❌ Você não tem permissão para usar este comando!")
        return
    
    # Verificar hierarquia de cargos
    if cargo >= interaction.user.top_role:
        await interaction.response.send_message("❌ Você só pode remover cargos menores que o seu cargo mais alto!")
        return
    
    try:
        await membro.remove_roles(cargo)
        embed = discord.Embed(
            title="Cargo Removido",
            description=f"{membro.mention} teve o cargo {cargo.mention} removido",
            color=discord.Color.purple()
        )
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Não tenho permissão para remover este cargo! Verifique se meu cargo está acima do cargo a ser removido.")
    except Exception as e:
        await interaction.response.send_message(f"❌ Erro ao remover cargo: {str(e)}")

@bot_staff.tree.command(name="embed", description="Criar um embed customizado")
@discord.app_commands.describe(
    titulo="Título do embed",
    descricao="Descrição do embed",
    cor="Cor (vermelho, azul, verde, amarelo, roxo, laranja, rosa, branco, preto, teal) ou hex (ex: FF0000)"
)
async def slash_embed(interaction: discord.Interaction, titulo: str, descricao: str, cor: str = "azul"):
    if interaction.guild_id != SERVIDOR_ID:
        await interaction.response.send_message("❌ Este comando só pode ser usado no servidor autorizado!")
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Apenas administradores podem usar este comando!")
        return
    
    # Mapeamento de cores por nome
    cores_mapeadas = {
        "vermelho": discord.Color.red(),
        "azul": discord.Color.blue(),
        "verde": discord.Color.green(),
        "amarelo": discord.Color.gold(),
        "roxo": discord.Color.purple(),
        "laranja": discord.Color.orange(),
        "rosa": discord.Color.magenta(),
        "branco": discord.Color.from_rgb(255, 255, 255),
        "preto": discord.Color.from_rgb(0, 0, 0),
        "teal": discord.Color.teal(),
    }
    
    try:
        # Verificar se é uma cor nomeada
        if cor.lower() in cores_mapeadas:
            cor_final = cores_mapeadas[cor.lower()]
        else:
            # Tentar parsear como hexadecimal
            try:
                cor_hex = int(cor.replace("#", ""), 16)
                cor_final = discord.Color(cor_hex)
            except ValueError:
                await interaction.response.send_message(f"❌ Cor inválida! Use um nome (vermelho, azul, verde, etc) ou hex (FF0000)")
                return
        
        embed = discord.Embed(
            title=titulo,
            description=descricao,
            color=cor_final
        )
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"❌ Erro ao criar embed: {str(e)}")

@ban.error
@mute.error
@unmute.error
@kick.error
@lock.error
@unlock.error
async def staff_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão para usar este comando!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Argumentos faltando!")

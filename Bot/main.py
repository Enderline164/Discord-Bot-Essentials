import os
import discord
from discord import app_commands
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
import random
from discord.ext import commands, tasks
import asyncio
from discord.ui import View, Button
from typing import List

#Configs - Variables

COIN_NAME = "Coins"

BOAS_VINDAS_DM_ATIVA = True
BOAS_VINDAS_PUBLICA_ATIVA = True

Welcome_Channel = "Canal-De-Boas-Vindas"

Mensagem_Publica = (
    "👋 Olá {mention}, seja muito bem-vindo(a) ao servidor **{server}**!\n"
    "Fique à vontade para explorar os canais e conversar com a galera!"
)

Mensagem_DM = (
    "Seja muito bem-vindo(a) ao servidor **Seu Servidor**, {name}! 🎉\n\n"
    "Aqui é o lugar perfeito pra você se divertir, fazer amizades e aproveitar tudo que preparamos com muito carinho.\n\n"
    "📌 Leia as regras, fique à vontade para perguntar qualquer coisa e bora fazer parte da nossa comunidade! 🚀\n\n"
    "💙 Qualquer coisa, é só chamar a equipe ou falar comigo. Estarei aqui para ajudar sempre!\n\n"
)

GUILD_ID = SERVER_ID
LOJA_DE_CARGOS = {
    "✨| Vip": 11500,
}
LOOT_BOX_PRICE = 500
LOOT_REWARDS = [
    {"type": "coins", "amount": 300, "chance": 40},
    {"type": "coins", "amount": 1000, "chance": 10},
    {"type": "xp", "amount": 50, "chance": 30},
    {"type": "xp", "amount": 150, "chance": 10},
    {"type": "role", "role_name": "LootBox Winner", "duration_minutes": 60, "chance": 10}
]

PROMO_CODES = {
    "BOASVINDAS": {"coins": 1500, "xp": 500},
}

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = ID
DATA_FILE = "economy.json"

class DiscordBotEssentials(discord.Client):

    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.data = {"users": {}, "daily_cooldown": {}, "transactions": []}
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = {"users": {}, "daily_cooldown": {}, "transactions": []}

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def get_user(self, user_id: int):
        return self.data["users"].setdefault(str(user_id), {
            "coins": 0,
            "xp": 0,
            "infinite": False,
            "badges": []
        })

    async def setup_hook(self):
        await self.tree.sync()
        print("Comandos sincronizados com sucesso!")

    async def on_ready(self):
        print(f"O Bot {self.user} foi ligado com sucesso.")
        await self.change_presence(activity=discord.Game(name="Minecraft"))

    def log_transaction(self, from_user, to_user, trans_type, amount, description=""):
        transaction = {
            "from": from_user,
            "to": to_user,
            "type": trans_type,
            "amount": amount,
            "timestamp": datetime.utcnow().isoformat(),
            "description": description
        }
        self.data["transactions"].append(transaction)
        self.save_data()

    def add_coins(self, user_id: int, amount: int):
        user = self.get_user(user_id)
        if not user.get("infinite", False):
            user["coins"] = max(user.get("coins", 0) + amount, 0)
            self.save_data()

    def remove_coins(self, user_id: int, amount: int):
        user = self.get_user(user_id)
        if not user.get("infinite", False):
            user["coins"] = max(user.get("coins", 0) - amount, 0)
            self.save_data()

    def add_xp(self, user_id: int, amount: int):
        user = self.get_user(user_id)
        user["xp"] = max(user.get("xp", 0) + amount, 0)
        self.save_data()

    def set_coins(self, user_id: int, amount: int):
        user = self.get_user(user_id)
        user["coins"] = amount
        self.save_data()

    def set_infinite(self, user_id: int, value: bool):
        user = self.get_user(user_id)
        user["infinite"] = value
        self.save_data()

    def can_claim_daily(self, user_id: int):
        last_str = self.data["daily_cooldown"].get(str(user_id))
        if last_str is None:
            return True
        last = datetime.fromisoformat(last_str)
        return (datetime.utcnow() - last) > timedelta(hours=24)

    def update_daily_claim(self, user_id: int):
        self.data["daily_cooldown"][str(user_id)] = datetime.utcnow().isoformat()
        self.save_data()

    def give_lootbox_reward(self, user_id):
        total_chance = sum(r["chance"] for r in LOOT_REWARDS)
        pick = random.uniform(0, total_chance)
        cumulative = 0
        for reward in LOOT_REWARDS:
            cumulative += reward["chance"]
            if pick <= cumulative:
                if reward["type"] == "coins":
                    self.add_coins(user_id, reward["amount"])
                elif reward["type"] == "xp":
                    self.add_xp(user_id, reward["amount"])
                return reward
        return {"type": "coins", "amount": 300} 

    def open_lootbox(self, user_id):
        user = self.get_user(user_id)
        if user["coins"] >= LOOT_BOX_PRICE:
            user["coins"] -= LOOT_BOX_PRICE
            self.log_transaction(user_id, "system", "purchase", LOOT_BOX_PRICE, "Compra de lootbox")
            reward = self.give_lootbox_reward(user_id)
            self.log_transaction("system", user_id, "reward", reward.get("amount", 0), f"Recompensa lootbox: {reward['type']}")
            if reward.get("type") == "role":
                self.add_badge(user_id, "lootbox_winner")
            self.save_data()
        else:
            print("Moedas insuficientes!")

    def is_admin(self, user: discord.User, guild: discord.Guild):
        member = guild.get_member(user.id)
        if user.id == OWNER_ID:
            return True
        if member is None:
            return False
        return member.guild_permissions.administrator or member.guild_permissions.manage_roles
    
    async def setup_hook(self):
        await self.tree.sync()
        print("Comandos sincronizados com sucesso!")

    async def on_ready(self):
        print(f"O Bot {self.user} foi ligado com sucesso.")
        await self.change_presence(activity=discord.Game(name="Minecraft"))

intents = discord.Intents.default()
intents.members = True

bot = DiscordBotEssentials()
client = DiscordBotEssentials()

def is_owner():
    def predicate(interaction: discord.Interaction):
        return interaction.user.id == OWNER_ID
    return app_commands.check(predicate)

def has_mod_permission():
    def predicate(interaction: discord.Interaction):
        perms = interaction.user.guild_permissions
        return perms.kick_members or perms.ban_members or interaction.user.id == OWNER_ID
    return app_commands.check(predicate)

@bot.event
async def on_member_join(member: discord.Member):
    guild = member.guild

    if BOAS_VINDAS_PUBLICA_ATIVA:
        channel = discord.utils.get(guild.text_channels, name=Welcome_Channel)
        if channel:
            try:
                await channel.send(
                    Mensagem_Publica.format(
                        mention=member.mention,
                        server=guild.name
                    )
                )
            except Exception as e:
                print(f"❌ Erro ao enviar mensagem pública: {e}")
        else:
            print(f"❌ Canal '{Welcome_Channel}' não encontrado no servidor '{guild.name}'.")

    if BOAS_VINDAS_DM_ATIVA:
        try:
            await member.send(Mensagem_DM.format(name=member.name))
        except Exception as e:
            print(f"❌ Não consegui enviar DM para {member.name}: {e}")

@bot.tree.command(name="avatar", description="Mostra o avatar de um usuário")
@app_commands.describe(membro="Usuário para ver o avatar (opcional)")
async def avatar(interaction: discord.Interaction,
                 membro: discord.Member = None):
    membro = membro or interaction.user
    embed = discord.Embed(title=f"Avatar de {membro}",
                          color=discord.Color.blue())
    embed.set_image(url=membro.display_avatar.url)
    embed.set_footer(text=f"ID: {membro.id}")
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="serverinfo",
                  description="Mostra informações do servidor")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild

    total_members = guild.member_count
    online_members = sum(m.status != discord.Status.offline
                         for m in guild.members)
    bot_count = sum(m.bot for m in guild.members)
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    roles_count = len(guild.roles)
    owner = guild.owner

    embed = discord.Embed(title=f"Informações do Servidor: {guild.name}",
                          color=discord.Color.green())
    embed.set_thumbnail(
        url=guild.icon.url if guild.icon else discord.Embed.Empty)
    embed.add_field(name="ID do Servidor", value=guild.id, inline=False)
    embed.add_field(name="Dono do Servidor",
                    value=f"{owner} (ID: {owner.id})",
                    inline=False)
    embed.add_field(name="Data de Criação",
                    value=guild.created_at.strftime("%d/%m/%Y"),
                    inline=False)
    embed.add_field(name="Membros Totais", value=total_members, inline=True)
    embed.add_field(name="Membros Online", value=online_members, inline=True)
    embed.add_field(name="Bots", value=bot_count, inline=True)
    embed.add_field(name="Canais de Texto", value=text_channels, inline=True)
    embed.add_field(name="Canais de Voz", value=voice_channels, inline=True)
    embed.add_field(name="Total de Cargos", value=roles_count, inline=True)
    embed.add_field(
        name="Região do Servidor",
        value=str(guild.region) if hasattr(guild, 'region') else "N/A",
        inline=True)

    await interaction.response.send_message(embed=embed)
from discord.ui import Modal, TextInput
from discord import TextStyle, Interaction, Embed, Color

class EmbedModal(Modal, title="Criar Embed"):

    titulo = TextInput(label="Título", placeholder="Digite o título do embed", max_length=256)
    descricao = TextInput(label="Descrição", placeholder="Digite a descrição", style=TextStyle.paragraph)
    canal_id = TextInput(label="ID do canal", placeholder="Ex: 123456789012345678")
    cor = TextInput(label="Cor (hex, opcional)", required=False, placeholder="#7289DA")
    imagem = TextInput(label="URL da imagem (opcional)", required=False, placeholder="https://exemplo.com/imagem.png")

    async def on_submit(self, interaction: Interaction):
        try:
            canal = interaction.guild.get_channel(int(self.canal_id.value))
            if not canal:
                await interaction.response.send_message("❌ Canal não encontrado!", ephemeral=True)
                return

            embed = Embed(
                title=self.titulo.value,
                description=self.descricao.value,
                color=Color.from_str(self.cor.value) if self.cor.value else Color.blurple()
            )

            if self.imagem.value:
                embed.set_image(url=self.imagem.value)

            await canal.send(embed=embed)
            await interaction.response.send_message("✅ Embed enviado com sucesso!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Erro ao enviar embed: `{e}`", ephemeral=True)
@bot.tree.command(name="embed_criar", description="Cria um embed visual com modal")
@has_mod_permission()
async def embed_criar(interaction: discord.Interaction):
    await interaction.response.send_modal(EmbedModal())

@bot.tree.command(name="embed_enviar", description="Envia o embed criado para um canal")
@has_mod_permission()
@app_commands.describe(canal="Canal para enviar o embed")
async def embed_enviar(interaction: discord.Interaction, canal: discord.TextChannel):
    dados = bot.user_embeds.get(str(interaction.user.id))
    if not dados:
        await interaction.response.send_message("Você ainda não criou um embed com `/embed_criar`.", ephemeral=True)
        return

    embed = discord.Embed(
        title=dados["title"],
        description=dados["description"],
        color=dados["color"]
    )
    embed.set_footer(text=f"Enviado por {interaction.user}", icon_url=interaction.user.display_avatar.url)

    await canal.send(embed=embed)
    await interaction.response.send_message(f"Embed enviado em {canal.mention}!", ephemeral=True)


@bot.tree.command(
    name="say",
    description="Envia uma mensagem simples em um canal específico")
@has_mod_permission()
@app_commands.describe(canal="Canal para enviar a mensagem",
                       mensagem="Mensagem para enviar")
async def say(interaction: discord.Interaction, canal: discord.TextChannel,
              mensagem: str):
    await canal.send(mensagem)
    await interaction.response.send_message(
        f"Mensagem enviada em {canal.mention}!", ephemeral=True)


@bot.tree.command(name="dm",
                  description="Envia uma mensagem direta (DM) para um usuário")
@has_mod_permission()
@app_commands.describe(usuario="Usuário para enviar a DM",
                       mensagem="Mensagem para enviar")
async def dm(interaction: discord.Interaction, usuario: discord.User,
             mensagem: str):
    try:
        await usuario.send(mensagem)
        await interaction.response.send_message(
            f"Mensagem enviada para {usuario.mention}!", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message(
            "Não foi possível enviar DM para este usuário.", ephemeral=True)


@bot.tree.command(name="ping", description="Responde com Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! 🏓")

@bot.tree.command(name="ship", description="Veja o nível de amor entre dois usuários!")
@app_commands.describe(user1="Primeiro usuário", user2="Segundo usuário")
async def ship(interaction: discord.Interaction, user1: discord.User, user2: discord.User):
    if user1.id == user2.id:
        await interaction.response.send_message("Você não pode shippar a mesma pessoa consigo mesma! 😅", ephemeral=True)
        return

    porcentagem = random.randint(0, 100)

    if porcentagem >= 90:
        status = "💘 Alma gêmea!"
    elif porcentagem >= 70:
        status = "💖 Casal perfeito!"
    elif porcentagem >= 50:
        status = "💕 Tem química!"
    elif porcentagem >= 30:
        status = "💔 Melhor só amizade..."
    else:
        status = "❌ Não combinam nem no Uno."

    barra = "█" * (porcentagem // 10) + "░" * (10 - (porcentagem // 10))

    embed = discord.Embed(
        title="💞 Calculadora do Amor 💞",
        description=(
            f"**{user1.mention}** + **{user2.mention}**\n\n"
            f"💟 Compatibilidade: `{porcentagem}%`\n"
            f"`{barra}`\n\n"
            f"📊 Resultado: **{status}**"
        ),
        color=discord.Color.magenta()
    )
    embed.set_footer(text="❤️ Ship")

    await interaction.response.send_message(embed=embed)

class SorteioView(View):
    def __init__(self, timeout: int):
        super().__init__(timeout=timeout * 60)
        self.participantes: List[int] = []

    @discord.ui.button(label="🎉 Participar", style=discord.ButtonStyle.success)
    async def participar(self, interaction: discord.Interaction, button: Button):
        user_id = interaction.user.id
        if user_id in self.participantes:
            await interaction.response.send_message("Você já está participando do sorteio!", ephemeral=True)
        else:
            self.participantes.append(user_id)
            await interaction.response.send_message("🎉 Você entrou no sorteio!", ephemeral=True)
             
@bot.tree.command(name="sorteio", description="Inicia um sorteio com tempo e prêmio definido.")
@app_commands.describe(premio="O que será sorteado", tempo="Tempo (em minutos)", descricao="Descrição opcional")
@has_mod_permission()
async def sorteio(interaction: discord.Interaction, premio: str, tempo: int, descricao: str = "Clique no botão para participar!"):
    if tempo <= 0 or tempo > 1440:
        await interaction.response.send_message("⚠️ Defina um tempo entre 1 e 1440 minutos.", ephemeral=True)
        return

    embed = discord.Embed(
        title="🎁 Sorteio Iniciado!",
        description=f"**Prêmio:** {premio}\n\n{descricao}",
        color=discord.Color.gold()
    )
    embed.set_footer(text=f"⏰ Termina em {tempo} minuto(s) • Criado por {interaction.user.display_name}")
    
    view = SorteioView(timeout=tempo)
    message = await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message("✅ Sorteio criado com sucesso!", ephemeral=True)

    await view.wait()

    if view.participantes:
        vencedor_id = random.choice(view.participantes)
        vencedor = await bot.fetch_user(vencedor_id)

        result_embed = discord.Embed(
            title="🏆 Resultado do Sorteio!",
            description=f"O vencedor do sorteio de **{premio}** é {vencedor.mention}! 🎉",
            color=discord.Color.green()
        )
        await message.reply(embed=result_embed)
    else:
        cancel_embed = discord.Embed(
            title="❌ Sorteio cancelado",
            description="Ninguém participou do sorteio.",
            color=discord.Color.red()
        )
        await message.reply(embed=cancel_embed)             

@bot.tree.command(name="info", description="Informações do bot e do servidor")
async def info(interaction: discord.Interaction):
    embed = discord.Embed(title="Informações", color=discord.Color.blue())
    embed.add_field(name="Bot",
                    value=f"{bot.user} (ID: {bot.user.id})",
                    inline=False)
    embed.add_field(
        name="Servidor",
        value=f"{interaction.guild.name} (ID: {interaction.guild.id})",
        inline=False)
    embed.add_field(name="Membros",
                    value=str(interaction.guild.member_count),
                    inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="warn", description="Avisa um usuário com um motivo.")
@app_commands.describe(user="Usuário a ser avisado", motivo="Motivo do aviso")
@has_mod_permission()
async def warn(interaction: discord.Interaction, user: discord.User, motivo: str):
    user_data = bot.get_user(user.id)
    warns = user_data.setdefault("warns", [])
    aviso = {
        "moderador": interaction.user.name,
        "motivo": motivo,
        "data": datetime.utcnow().strftime("%d/%m/%Y %H:%M")
    }
    warns.append(aviso)
    bot.save_data()

    embed = discord.Embed(
        title="⚠️ Aviso Registrado",
        description=f"{user.mention} recebeu um aviso!",
        color=discord.Color.orange()
    )
    embed.add_field(name="👮 Moderador", value=interaction.user.mention, inline=True)
    embed.add_field(name="📄 Motivo", value=motivo, inline=False)
    embed.set_footer(text=f"Total de avisos: {len(warns)}")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="desligar", description="Desliga o bot (somente dono)")
@is_owner()
async def desligar(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Desligando o bot...")
    await bot.close()

import random

@bot.tree.command(name="verwarns", description="Veja os avisos de um usuário.")
@app_commands.describe(user="Usuário para ver os avisos")
@has_mod_permission()
async def verwarns(interaction: discord.Interaction, user: discord.User):
    user_data = bot.get_user(user.id)
    warns = user_data.get("warns", [])

    if not warns:
        await interaction.response.send_message(f"{user.mention} não possui nenhum aviso!", ephemeral=True)
        return

    embed = discord.Embed(
        title=f"📋 Avisos de {user.name}",
        color=discord.Color.red()
    )

    for idx, aviso in enumerate(warns[-10:], start=1):  
        embed.add_field(
            name=f"Aviso {idx}",
            value=f"**Motivo:** {aviso['motivo']}\n**Moderador:** {aviso['moderador']}\n**Data:** {aviso['data']}",
            inline=False
        )

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="lootbox", description="Abra uma lootbox e ganhe recompensas aleatórias!")
async def lootbox(interaction: discord.Interaction):
    COST = 500 
    user_data = bot.get_user(interaction.user.id)

    if user_data.get("infinite", False):
        can_pay = True
    else:
        can_pay = user_data.get("coins", 0) >= COST

    if not can_pay:
        await interaction.response.send_message(f"❌ Você precisa de pelo menos {COST} Coins para abrir uma lootbox.", ephemeral=True)
        return

    if not user_data.get("infinite", False):
        bot.remove_coins(interaction.user.id, COST)

    premios = [
        ("coins", random.randint(100, 3000), 0.5),
        ("xp", random.randint(10, 500), 0.3),    
        ("nada", 0, 0.2)                         
    ]

    escolha = random.choices(premios, weights=[p[2] for p in premios], k=1)[0]

    if escolha[0] == "coins":
        bot.add_coins(interaction.user.id, escolha[1])
        premio_msg = f"Você ganhou **{escolha[1]}** {COIN_NAME}! 🪙"
    elif escolha[0] == "xp":
        bot.add_xp(interaction.user.id, escolha[1])
        premio_msg = f"Você ganhou **{escolha[1]}** XP! 📘"
    else:
        premio_msg = "Infelizmente, você não ganhou nada desta vez... 😢"

    embed = discord.Embed(
        title="🎁 Lootbox Aberta!",
        description=premio_msg,
        color=discord.Color.gold()
    )
    embed.set_footer(text=f"Custo para abrir: {COST} {COIN_NAME}")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="limpar", description="Limpa mensagens de um canal.")
@app_commands.describe(quantidade="Número de mensagens para apagar (máx: 100)")
@has_mod_permission()
async def limpar(interaction: discord.Interaction, quantidade: int):
    if quantidade <= 0 or quantidade > 100:
        await interaction.response.send_message("⚠️ Informe um número entre 1 e 100.", ephemeral=True)
        return

    await interaction.response.defer(thinking=True) 

    def check(msg):
        return True 

    apagadas = await interaction.channel.purge(limit=quantidade, check=check)

    confirm = discord.Embed(
        title="🧹 Limpeza realizada",
        description=f"{len(apagadas)} mensagens foram apagadas por {interaction.user.mention}.",
        color=discord.Color.green()
    )
    await interaction.followup.send(embed=confirm, ephemeral=True)

@bot.tree.command(name="votacao", description="Cria uma votação com múltiplas opções.")
@app_commands.describe(
    titulo="Título da votação",
    descricao="Descrição da votação",
    opcoes="Opções separadas por vírgula (ex: Azul, Verde, Vermelho)"
)
@has_mod_permission()
async def votacao(interaction: discord.Interaction, titulo: str, descricao: str, opcoes: str):
    opcoes_lista = [opcao.strip() for opcao in opcoes.split(",") if opcao.strip()]

    if len(opcoes_lista) < 2 or len(opcoes_lista) > 10:
        await interaction.response.send_message("⚠️ Forneça entre 2 e 10 opções separadas por vírgula.", ephemeral=True)
        return

    emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

    embed = discord.Embed(
        title=f"📊 {titulo}",
        description=descricao,
        color=discord.Color.blue()
    )

    for i, opcao in enumerate(opcoes_lista):
        embed.add_field(name=f"{emojis[i]} {opcao}", value="\u200b", inline=False)

    embed.set_footer(text=f"Votação criada por {interaction.user.display_name}")

    mensagem = await interaction.channel.send(embed=embed)

    for i in range(len(opcoes_lista)):
        await mensagem.add_reaction(emojis[i])

    await interaction.response.send_message("✅ Votação criada com sucesso!", ephemeral=True)

@bot.tree.command(name="loja", description="Veja os cargos disponíveis para compra")
async def loja(interaction: discord.Interaction):
    embed = discord.Embed(title="🛒 Loja de Cargos", color=discord.Color.purple())
    for cargo, preco in LOJA_DE_CARGOS.items():
        embed.add_field(name=cargo, value=f"{preco} {COIN_NAME}", inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="comprar", description="Compre um Cargos")
@app_commands.describe(nome_do_cargo="Nome exato do cargo que deseja comprar")
async def comprar(interaction: discord.Interaction, nome_do_cargo: str):
    cargo_nome = nome_do_cargo.strip()

    if cargo_nome not in LOJA_DE_CARGOS:
        await interaction.response.send_message("❌ Cargo não encontrado na loja. Use `/loja` para ver os disponíveis.", ephemeral=True)
        return

    preco = LOJA_DE_CARGOS[cargo_nome]
    user_data = bot.get_user(interaction.user.id)

    if user_data.get("infinite", False) or user_data.get("coins", 0) >= preco:
        guild = interaction.guild
        cargo = discord.utils.get(guild.roles, name=cargo_nome)

        if not cargo:
            await interaction.response.send_message("❌ Cargo não encontrado no servidor.", ephemeral=True)
            return

        await interaction.user.add_roles(cargo)
        if not user_data.get("infinite", False):
            bot.remove_coins(interaction.user.id, preco)

        await interaction.response.send_message(
            f"✅ Você comprou o cargo **{cargo.name}** por {preco} {COIN_NAME}!", ephemeral=True
        )
    else:
        await interaction.response.send_message("❌ Você não tem {COIN_NAME} suficientes.", ephemeral=True)

@bot.tree.command(name="status",
                  description="Muda o status do bot (somente dono)")
@app_commands.describe(jogo="Novo status para o bot")
@is_owner()
async def status(interaction: discord.Interaction, jogo: str):
    await bot.change_presence(activity=discord.Game(name=jogo))
    await interaction.response.send_message(
        f"Status alterado para: Jogando {jogo}")

@bot.tree.command(name="coins", description="Mostra a sua econômia")
async def coins(interaction: discord.Interaction):
    user = bot.get_user(interaction.user.id)
    inf = user.get("infinite", False)
    coins = "∞" if inf else user.get("coins", 0)
    await interaction.response.send_message(
        f"{interaction.user.mention}, você tem **{coins}** {COIN_NAME}.")

@bot.tree.command(name="resgatar")
@app_commands.describe(codigo="Código promocional para resgatar")
async def resgatar(interaction: discord.Interaction, codigo: str):
    user_id = interaction.user.id
    code = codigo.upper()

    user = bot.get_user(user_id)

    if code not in PROMO_CODES:
        await interaction.response.send_message("❌ Código inválido ou expirado!", ephemeral=True)
        return

    user_claims = user.setdefault("claimed_codes", [])
    if code in user_claims:
        await interaction.response.send_message("❌ Você já usou este código antes!", ephemeral=True)
        return

    reward = PROMO_CODES[code]

    coins = reward.get("coins", 0)
    xp = reward.get("xp", 0)
    badge = reward.get("badge", None)

    if coins > 0:
        bot.add_coins(user_id, coins)
    if xp > 0:
        bot.add_xp(user_id, xp)
    if badge:
        bot.add_badge(user_id, badge)

    user_claims.append(code)
    bot.save_data()

    await interaction.response.send_message(
        f"🎉 Código resgatado com sucesso! Você recebeu:\n"
        f"💰 {coins} {COIN_NAME}\n"
        f"⭐ {xp} XP\n"
        + (f"🏅 Badge: {badge}" if badge else ""),
        ephemeral=True
    )

@bot.tree.command(name="xp", description="Mostra seu XP")
async def xp(interaction: discord.Interaction):
    user = bot.get_user(interaction.user.id)
    await interaction.response.send_message(
        f"{interaction.user.mention}, você tem **{user.get('xp', 0)}** XP.")


@bot.tree.command(
    name="daily",
    description="Pegue sua recompensa diária (24h)")
async def daily(interaction: discord.Interaction):
    user_id = interaction.user.id
    if not bot.can_claim_daily(user_id):
        last = datetime.fromisoformat(bot.data["daily_cooldown"][str(user_id)])
        next_time = last + timedelta(hours=24)
        diff = next_time - datetime.utcnow()
        await interaction.response.send_message(
            f"Você já coletou sua recompensa diária! Tente novamente em {str(diff).split('.')[0]}"
        )
        return

    reward = 100
    xp_reward = 10
    bot.add_coins(user_id, reward)
    bot.add_xp(user_id, xp_reward)
    bot.update_daily_claim(user_id)
    await interaction.response.send_message(
        f"Você coletou {reward} {COIN_NAME} e {xp_reward} XP! Volte amanhã para mais."
    )


@bot.tree.command(name="pay",
                  description="Pague outro membro")
@app_commands.describe(membro="Membro que vai receber",
                       quantidade="Quantidade de moedas para pagar")
async def pay(interaction: discord.Interaction, membro: discord.Member,
              quantidade: int):
    if quantidade <= 0:
        await interaction.response.send_message(
            "Digite uma quantidade válida (> 0).")
        return

    payer_id = interaction.user.id
    receiver_id = membro.id
    if membro.bot:
        await interaction.response.send_message("Você não pode pagar um bot.")
        return

    payer = bot.get_user(payer_id)
    if payer.get("infinite", False):
        bot.add_coins(receiver_id, quantidade)
        bot.add_xp(receiver_id, quantidade // 10) 
        await interaction.response.send_message(
            f"{interaction.user.mention} pagou {quantidade} {COIN_NAME} para {membro.mention} (pagador tem dinheiro infinito)."
        )
        return

    if payer.get("coins", 0) < quantidade:
        await interaction.response.send_message(
            "Você não tem {COIN_NAME} suficientes.")
        return

    bot.remove_coins(payer_id, quantidade)
    bot.add_coins(receiver_id, quantidade)
    bot.add_xp(payer_id, quantidade // 10)
    bot.add_xp(receiver_id, quantidade // 10)

    await interaction.response.send_message(
        f"{interaction.user.mention} pagou {quantidade} {COIN_NAME} para {membro.mention}."
    )

@bot.tree.command(
    name="setcoins",
    description="Define o dinheiro de um usuário (somente dono)")
@is_owner()
@app_commands.describe(membro="Membro para alterar",
                       quantidade="Quantidade de moedas")
async def setcoins(interaction: discord.Interaction, membro: discord.Member,
                   quantidade: int):
    if quantidade < 0:
        await interaction.response.send_message(
            "Quantidade não pode ser negativa.")
        return
    bot.set_coins(membro.id, quantidade)
    await interaction.response.send_message(
        f"Setei {quantidade} {COIN_NAME} para {membro.mention}.")

@bot.tree.command(name="statusconfig", description="Altera o tipo de status do bot (somente dono)")
@is_owner()
@app_commands.describe(tipo="Tipo de status (jogando, transmitindo, ouvindo, assistindo)", texto="Texto do status")
async def statusconfig(interaction: discord.Interaction, tipo: str, texto: str):
    tipo = tipo.lower()

    if tipo == "jogando":
        activity = discord.Game(name=texto)
    elif tipo == "transmitindo":
        activity = discord.Streaming(name=texto, url="https://twitch.tv/seucanal")
    elif tipo == "ouvindo":
        activity = discord.Activity(type=discord.ActivityType.listening, name=texto)
    elif tipo == "assistindo":
        activity = discord.Activity(type=discord.ActivityType.watching, name=texto)
    else:
        await interaction.response.send_message("❌ Tipo inválido. Use: jogando, transmitindo, ouvindo ou assistindo.", ephemeral=True)
        return

    await bot.change_presence(activity=activity)
    await interaction.response.send_message(f"✅ Status atualizado para: {tipo.title()} {texto}", ephemeral=True)

@bot.tree.command(name="leaderboard_xp", description="Mostra o top 10 de XP")
async def leaderboard_xp(interaction: discord.Interaction):
    users = bot.data["users"]
    ranked = sorted(users.items(), key=lambda x: x[1].get("xp", 0), reverse=True)

    embed = discord.Embed(title="📘 Top 10 - XP", color=discord.Color.purple())
    for i, (user_id, data) in enumerate(ranked[:10], start=1):
        try:
            member = await interaction.guild.fetch_member(int(user_id))
            name = member.display_name
        except:
            name = f"Usuário {user_id}"
        embed.add_field(name=f"{i}. {name}", value=f"{data.get('xp', 0)} XP", inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="perfil", description="Mostra seu perfil de economia e XP")
async def perfil(interaction: discord.Interaction):
    user = bot.get_user(interaction.user.id)
    coins = "∞" if user.get("infinite", False) else user.get("coins", 0)
    xp = user.get("xp", 0)

    embed = discord.Embed(title=f"Perfil de {interaction.user.name}", color=discord.Color.gold())
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.add_field(name="💰 {COIN_NAME}", value=str(coins), inline=True)
    embed.add_field(name="📘 XP", value=str(xp), inline=True)
    embed.set_footer(text=f"ID do usuário: {interaction.user.id}")

    await interaction.response.send_message(embed=embed)


@bot.tree.command(
    name="setinfinite",
    description="Define se um usuário tem dinheiro infinito (somente dono)")
@is_owner()
@app_commands.describe(membro="Membro para alterar",
                       valor="True para infinito, False para normal")
async def setinfinite(interaction: discord.Interaction, membro: discord.Member,
                      valor: bool):
    bot.set_infinite(membro.id, valor)
    status = "infinito" if valor else "normal"
    await interaction.response.send_message(
        f"Dinheiro de {membro.mention} agora é {status}.")

@bot.tree.command(name="leaderboard_money",
                  description="Mostra o top 10 de money")
async def leaderboard_coins(interaction: discord.Interaction):
    users = bot.data["users"]

    ranked = sorted(users.items(),
                    key=lambda x: float('inf')
                    if x[1].get("infinite", False) else x[1].get("coins", 0),
                    reverse=True)

    embed = discord.Embed(title="🥇 Top 10 - {COIN_NAME}",
                          color=discord.Color.gold())
    for i, (user_id, data) in enumerate(ranked[:10], start=1):
        coins = "∞" if data.get("infinite", False) else data.get("coins", 0)
        try:
            member = await interaction.guild.fetch_member(int(user_id))
            name = member.display_name
        except:
            name = f"Usuário {user_id}"
        embed.add_field(name=f"{i}. {name}", value=f"{coins} 🪙", inline=False)

    await interaction.response.send_message(embed=embed)

import discord
from discord.ext import commands


@bot.event
async def on_ready():
    print(f'Bot {bot.user} está online!')


bot.run(TOKEN)

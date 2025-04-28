import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Carrega o .env
load_dotenv()

# Configuração de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX', '!')
OWNER_ID = int(os.getenv('OWNER_ID', 0))

# Verificação
if not TOKEN:
    logger.error("❌ DISCORD_TOKEN não encontrado! Defina no arquivo .env.")
    exit(1)
if OWNER_ID == 0:
    logger.warning("⚠️ OWNER_ID não configurado corretamente no .env!")

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

# Bot
bot = commands.Bot(command_prefix=PREFIX, owner_id=OWNER_ID, intents=intents)

# Evento de ready
@bot.event
async def on_ready():
    logger.info(f'✅ Logado como {bot.user} (ID: {bot.user.id})')
    logger.info('🔄 Carregando Cogs...')
    await load_cogs()
    logger.info('✅ Todos os Cogs carregados!')

# Função para carregar Cogs
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            cog = f'cogs.{filename[:-3]}'
            try:
                await bot.load_extension(cog)
                logger.info(f'🔁 Cog carregado: {cog}')
            except Exception as e:
                logger.error(f'❌ Erro ao carregar {cog}: {e}')

# Comando básico
@bot.command()
async def ping(ctx):
    await ctx.send('🏓 Pong!')

# Rodar o bot
if __name__ == "__main__":
    bot.run(TOKEN)

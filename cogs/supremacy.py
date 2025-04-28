from discord.ext import commands
from supremacy1914_wrapper import Supremacy

class SupremacyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sessions = {}  # Aqui vamos guardar as sessões dos usuários

    @commands.command()
    async def conectar(self, ctx, email: str, senha: str):
        """Conecta sua conta do Supremacy 1914."""
        try:
            supremacy = Supremacy()
            supremacy.login(email, senha)
            self.sessions[ctx.author.id] = supremacy
            await ctx.author.send("✅ Conta conectada com sucesso!")
        except Exception as e:
            await ctx.author.send(f"❌ Erro ao conectar: {str(e)}")

    @commands.command()
    async def perfil(self, ctx):
        """Mostra o perfil do jogador conectado."""
        supremacy = self.sessions.get(ctx.author.id)
        if not supremacy:
            await ctx.send("⚠️ Você precisa se conectar primeiro usando `!conectar <email> <senha>`.")
            return

        profile = supremacy.get_profile()
        await ctx.send(f"👤 Perfil de {profile['name']}:\nXP: {profile['experiencePoints']}\nNível: {profile['level']}")

    @commands.command()
    async def meus_jogos(self, ctx):
        """Mostra os jogos (mapas) que o jogador participa."""
        supremacy = self.sessions.get(ctx.author.id)
        if not supremacy:
            await ctx.send("⚠️ Você precisa se conectar primeiro usando `!conectar <email> <senha>`.")
            return

        games = supremacy.my_games()
        if not games:
            await ctx.send("🔍 Nenhum jogo encontrado.")
            return

        msg = "**Seus jogos:**\n"
        for game in games:
            msg += f"🌍 {game['name']} - ID: {game['id']} - Estado: {game['state']}\n"
        await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(SupremacyCog(bot))

import discord
from discord.ext import commands
import random
import json
import os
from datetime import datetime

class XP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = 'data/xp_data.json'
        self.user_xp = self.load_xp()

    def load_xp(self):
        """Carrega os dados de XP do arquivo JSON."""
        if os.path.exists(self.file):
            with open(self.file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_xp(self):
        """Salva os dados de XP no arquivo JSON."""
        with open(self.file, 'w', encoding='utf-8') as f:
            json.dump(self.user_xp, f, indent=4)

    def add_xp_to_user(self, user_id, min_xp=5, max_xp=15):
        """Adiciona XP ao usuário e salva os dados."""
        if user_id not in self.user_xp:
            self.user_xp[user_id] = {"xp": 0, "last_message": None}

        self.user_xp[user_id]["xp"] += random.randint(min_xp, max_xp)
        self.user_xp[user_id]["last_message"] = datetime.utcnow().isoformat()
        self.save_xp()

    @commands.Cog.listener()
    async def on_message(self, message):
        """Dá XP ao usuário sempre que ele enviar uma mensagem."""
        if message.author.bot:
            return  # Ignora mensagens de bots

        user_id = str(message.author.id)
        self.add_xp_to_user(user_id)

    @commands.command(name="xp")
    async def show_xp(self, ctx):
        """Mostra o XP atual do usuário."""
        user_id = str(ctx.author.id)
        user_data = self.user_xp.get(user_id, {"xp": 0, "last_message": None})

        last_msg = user_data["last_message"]
        if last_msg:
            last_msg = datetime.fromisoformat(last_msg).strftime('%d/%m/%Y %H:%M:%S')
        else:
            last_msg = "Nunca"

        await ctx.send(f"{ctx.author.mention}, você tem {user_data['xp']} XP! Última mensagem: {last_msg}")

    @commands.command(name="rank")
    async def show_rank(self, ctx):
        """Mostra o ranking geral de XP."""
        leaderboard = sorted(self.user_xp.items(), key=lambda x: x[1]["xp"], reverse=True)

        if not leaderboard:
            await ctx.send("Nenhum dado de XP encontrado!")
            return

        ranking = []
        for index, (user_id, xp_data) in enumerate(leaderboard[:10], start=1):
            user = self.bot.get_user(int(user_id))
            user_display = user.name if user else f"ID {user_id}"
            ranking.append(f"**{index}.** {user_display} — {xp_data['xp']} XP")

        embed = discord.Embed(
            title="🏆 Ranking de XP",
            description="\n".join(ranking),
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    @commands.command(name="resetxp")
    @commands.has_permissions(administrator=True)
    async def reset_xp(self, ctx, member: discord.Member):
        """Reseta o XP de um membro."""
        user_id = str(member.id)

        if user_id in self.user_xp:
            self.user_xp[user_id] = {"xp": 0, "last_message": None}
            self.save_xp()
            await ctx.send(f"O XP de {member.mention} foi resetado com sucesso!")
        else:
            await ctx.send(f"{member.mention} não possui dados de XP.")

async def setup(bot):
    await bot.add_cog(XP(bot))

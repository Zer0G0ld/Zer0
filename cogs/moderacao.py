import discord
from discord.ext import commands
import datetime

class Moderacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Comando para expulsar um membro
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Motivo não especificado"):
        """Expulsa um membro do servidor"""
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} foi expulso. Motivo: {reason}")

        # Logando a ação de kick
        log_channel = discord.utils.get(ctx.guild.text_channels, name="logs")  # Ajuste o nome do canal
        if log_channel:
            embed = discord.Embed(
                title="Ação de Moderação: Kick",
                description=f"{ctx.author} expulsou {member.mention}",
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()  # Timestamp correto
            )
            embed.add_field(name="Motivo", value=reason)
            embed.add_field(name="Data", value=discord.utils.format_dt(datetime.datetime.utcnow(), style="R"))
            await log_channel.send(embed=embed)

    # Comando para banir um membro
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Motivo não especificado"):
        """Bane um membro do servidor"""
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} foi banido. Motivo: {reason}")

        # Logando a ação de banimento
        log_channel = discord.utils.get(ctx.guild.text_channels, name="logs")  # Ajuste o nome do canal
        if log_channel:
            embed = discord.Embed(
                title="Ação de Moderação: Ban",
                description=f"{ctx.author} baniu {member.mention}",
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()  # Timestamp correto
            )
            embed.add_field(name="Motivo", value=reason)
            embed.add_field(name="Data", value=discord.utils.format_dt(datetime.datetime.utcnow(), style="R"))
            await log_channel.send(embed=embed)

    # Comando para desbanir um membro
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.User, *, reason="Motivo não especificado"):
        """Desbane um membro do servidor"""
        await ctx.guild.unban(member)
        await ctx.send(f"✅ {member.mention} foi desbanido. Motivo: {reason}")

        # Logando a ação de desbanimento
        log_channel = discord.utils.get(ctx.guild.text_channels, name="logs")  # Ajuste o nome do canal
        if log_channel:
            embed = discord.Embed(
                title="Ação de Moderação: Unban",
                description=f"{ctx.author} desbaniu {member.mention}",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()  # Timestamp correto
            )
            embed.add_field(name="Motivo", value=reason)
            embed.add_field(name="Data", value=discord.utils.format_dt(datetime.datetime.utcnow(), style="R"))
            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderacao(bot))
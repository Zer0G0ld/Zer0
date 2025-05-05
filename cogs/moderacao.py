import discord
from discord.ext import commands
import datetime
import re
import json
import os

# Carregar e salvar os avisos de forma segura
WARN_FILE = "warns.json"

if os.path.exists(WARN_FILE):
    with open(WARN_FILE, "r", encoding="utf-8") as f:
        warns = json.load(f)
else:
    warns = {}

def save_warns():
    with open(WARN_FILE, "w", encoding="utf-8") as f:
        json.dump(warns, f, indent=4)

class Moderacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_log_channel(self, ctx):
        return discord.utils.get(ctx.guild.text_channels, name="logs")

    async def send_log(self, ctx, title, description, color, **fields):
        log_channel = self.get_log_channel(ctx)
        if log_channel:
            embed = discord.Embed(
                title=title,
                description=description,
                color=color,
                timestamp=datetime.datetime.utcnow()
            )
            for name, value in fields.items():
                embed.add_field(name=name, value=value)
            await log_channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Motivo não especificado"):
        """Expulsa um membro do servidor"""
        try:
            await member.kick(reason=reason)
            await ctx.send(f"👢 {member.mention} foi expulso. Motivo: {reason}")
            await self.send_log(ctx, "Ação de Moderação: Kick", f"{ctx.author} expulsou {member.mention}", discord.Color.red(), Motivo=reason)
        except discord.Forbidden:
            await ctx.send("❌ Não tenho permissão para expulsar esse membro.")
        except Exception as e:
            await ctx.send("❌ Ocorreu um erro ao expulsar o membro.")
            raise e

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Motivo não especificado"):
        """Bane um membro do servidor"""
        try:
            await member.ban(reason=reason)
            await ctx.send(f"🔨 {member.mention} foi banido. Motivo: {reason}")
            await self.send_log(ctx, "Ação de Moderação: Ban", f"{ctx.author} baniu {member.mention}", discord.Color.red(), Motivo=reason)
        except discord.Forbidden:
            await ctx.send("❌ Não tenho permissão para banir esse membro.")
        except Exception as e:
            await ctx.send("❌ Ocorreu um erro ao banir o membro.")
            raise e

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.User, *, reason="Motivo não especificado"):
        """Desbane um membro do servidor"""
        try:
            await ctx.guild.unban(member)
            await ctx.send(f"✅ {member.mention} foi desbanido. Motivo: {reason}")
            await self.send_log(ctx, "Ação de Moderação: Unban", f"{ctx.author} desbaniu {member.mention}", discord.Color.green(), Motivo=reason)
        except discord.NotFound:
            await ctx.send("❌ Esse usuário não está banido.")
        except discord.Forbidden:
            await ctx.send("❌ Não tenho permissão para desbanir esse usuário.")
        except Exception as e:
            await ctx.send("❌ Ocorreu um erro ao desbanir o usuário.")
            raise e

    @commands.command(name="clear", aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, quantidade: int):
        """Apaga mensagens em massa (limite de 100)."""
        if quantidade > 100:
            await ctx.send("⚠️ O limite máximo é 100 mensagens.")
            return
        try:
            await ctx.channel.purge(limit=quantidade + 1)
            await ctx.send(f"🧹 {quantidade} mensagens apagadas por {ctx.author.mention}.", delete_after=5)
            await self.send_log(ctx, "Ação de Moderação: Clear", f"{ctx.author} apagou {quantidade} mensagens em {ctx.channel.mention}", discord.Color.orange())
        except Exception as e:
            await ctx.send("❌ Ocorreu um erro ao apagar as mensagens.")
            raise e

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason="Motivo não especificado"):
        """Silencia um membro impedindo-o de falar nos canais."""
        try:
            role = discord.utils.get(ctx.guild.roles, name="Mutado")
            if not role:
                role = await ctx.guild.create_role(name="Mutado")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(role, speak=False, send_messages=False)
            await member.add_roles(role)
            await ctx.send(f"🔇 {member.mention} foi silenciado. Motivo: {reason}")
            await self.send_log(ctx, "Ação de Moderação: Mute", f"{ctx.author} silenciou {member.mention}", discord.Color.dark_gray(), Motivo=reason)
        except Exception as e:
            await ctx.send("❌ Ocorreu um erro ao aplicar o mute.")
            raise e

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        """Remove o silêncio de um membro."""
        try:
            role = discord.utils.get(ctx.guild.roles, name="Mutado")
            if role and role in member.roles:
                await member.remove_roles(role)
                await ctx.send(f"🔊 {member.mention} foi desmutado.")
                await self.send_log(ctx, "Ação de Moderação: Unmute", f"{ctx.author} removeu o mute de {member.mention}", discord.Color.green())
            else:
                await ctx.send("⚠️ Esse usuário não está silenciado.")
        except Exception as e:
            await ctx.send("❌ Ocorreu um erro ao desmutar o usuário.")
            raise e

    @commands.command(name="userinfo", aliases=["user"])
    async def userinfo(self, ctx, member: discord.Member = None):
        """Mostra informações de um membro."""
        try:
            member = member or ctx.author
            embed = discord.Embed(
                title=f"Informações de {member}",
                color=member.color,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.add_field(name="ID", value=member.id)
            embed.add_field(name="Cargo mais alto", value=member.top_role.mention)
            embed.add_field(name="Entrou no servidor", value=discord.utils.format_dt(member.joined_at, style='R'))
            embed.add_field(name="Criou a conta", value=discord.utils.format_dt(member.created_at, style='R'))
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send("❌ Ocorreu um erro ao obter as informações.")
            raise e

    @commands.command(name="cargo", aliases=["addrole", "darcargo"])
    @commands.has_permissions(manage_roles=True)
    async def cargo(self, ctx, member: discord.Member, *, nome_do_cargo: str):
        """Atribui um cargo a um membro."""
        try:
            if ctx.message.role_mentions:
                cargo = ctx.message.role_mentions[0]
            else:
                nome_processado = re.sub(r"[^\w\s]", "", nome_do_cargo).strip().lower()
                cargo = discord.utils.find(lambda r: re.sub(r"[^\w\s]", "", r.name).strip().lower() == nome_processado, ctx.guild.roles)

            if not cargo:
                await ctx.send("❌ Cargo não encontrado.")
                return

            if cargo >= ctx.author.top_role and ctx.author != ctx.guild.owner:
                await ctx.send("⚠️ Você não pode atribuir um cargo igual ou superior ao seu.")
                return

            if cargo >= ctx.guild.me.top_role:
                await ctx.send("⚠️ Não posso atribuir esse cargo. Ele é superior ao meu.")
                return

            await member.add_roles(cargo)
            await ctx.send(f"✅ {member.mention} recebeu o cargo **{cargo.name}**.")
            await self.send_log(ctx, "Ação de Moderação: Cargo Atribuído", f"{ctx.author} deu o cargo **{cargo.name}** para {member.mention}", discord.Color.blue())
        except Exception as e:
            await ctx.send("❌ Ocorreu um erro ao atribuir o cargo.")
            raise e

    @commands.command(name="rmcargo", aliases=["removercargo", "tirarcargo"])
    @commands.has_permissions(manage_roles=True)
    async def rmcargo(self, ctx, member: discord.Member, cargo: discord.Role):
        """Remove um cargo de um membro."""
        try:
            if cargo.position >= ctx.guild.me.top_role.position:
                await ctx.send("❌ Não posso remover esse cargo. Ele é superior ao meu.")
                return

            await member.remove_roles(cargo)
            await ctx.send(f"✅ O cargo **{cargo.name}** foi removido de {member.mention}.")
            await self.send_log(ctx, "Ação de Moderação: Cargo Removido", f"{ctx.author} removeu o cargo **{cargo.name}** de {member.mention}", discord.Color.orange())
        except Exception as e:
            await ctx.send("❌ Ocorreu um erro ao remover o cargo.")
            raise e
        
    @commands.command(name="warn", aliases=["aviso", "avisar", "Aviso", "Avisar"])
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, motivo="Motivo não especificado"):
        """Avisa um membro por mau comportamento."""
        if str(member.id) not in warns:
            warns[str(member.id)] = []
        warns[str(member.id)].append({
            "moderador": str(ctx.author),
            "motivo": motivo,
            "data": datetime.datetime.utcnow().isoformat()
        })
        save_warns()
        await ctx.send(f"⚠️ {member.mention} foi avisado. Motivo: {motivo}")
        await self.send_log(ctx, "Ação de Moderação: Aviso", f"{ctx.author} avisou {member.mention}", discord.Color.gold(), Motivo=motivo)


    @commands.command(name="warns", aliases=["avisos", "meusavisos"])
    async def warns(self, ctx, member: discord.Member = None):
        """Mostra os avisos de um membro."""
        member = member or ctx.author
        user_warns = warns.get(str(member.id), [])
        if not user_warns:
            await ctx.send("✅ Esse membro não possui avisos.")
            return

        embed = discord.Embed(
            title=f"Avisos de {member}",
            color=discord.Color.orange(),
            timestamp=datetime.datetime.utcnow()
        )
        for i, warn in enumerate(user_warns, start=1):
            embed.add_field(
                name=f"Aviso {i}",
                value=f"**Motivo:** {warn['motivo']}\n**Moderador:** {warn['moderador']}\n**Data:** {warn['data']}",
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.command(name="clearwarns", aliases=["limparavisos", "resetavisos"])
    @commands.has_permissions(manage_messages=True)
    async def clearwarns(self, ctx, member: discord.Member):
        """Limpa todos os avisos de um membro."""
        if str(member.id) in warns:
            del warns[str(member.id)]
            save_warns()
            await ctx.send(f"✅ Todos os avisos de {member.mention} foram limpos.")
            await self.send_log(ctx, "Ação de Moderação: Limpar Avisos", f"{ctx.author} limpou os avisos de {member.mention}", discord.Color.green())
        else:
            await ctx.send("⚠️ Esse membro não possui avisos.")

    @commands.command(name="slowmode")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, segundos: int = 0):
        try:
            if segundos == 0:
                await ctx.channel.edit(slowmode_delay=segundos)
                await ctx.send("⏱️ Modo lento desativado.")
            elif segundos > 0:
                await ctx.channel.edit(slowmode_delay=segundos)
                await ctx.send(f"⏱️ Modo lento definido para `{segundos}` segundos.")
            elif segundos < 0:
                return await ctx.send("⛔ O tempo não pode ser negativo.")
            
        except Exception as e:
            await ctx.send("❌ Ocorreu um erro ao definir o modo lento.")
            raise e


    # Erros gerais de comandos
    @kick.error
    @ban.error
    @unban.error
    @clear.error
    @mute.error
    @unmute.error
    @cargo.error
    @rmcargo.error
    async def mod_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 Você não tem permissão para usar esse comando.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("⚠️ Argumento ausente. Verifique o uso correto do comando.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("⚠️ Argumento inválido. Verifique se o membro ou cargo está correto.")
        else:
            await ctx.send("❌ Um erro inesperado ocorreu.")
            raise error

async def setup(bot):
    await bot.add_cog(Moderacao(bot))

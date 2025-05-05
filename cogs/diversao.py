import asyncio
import random
import discord
import time
from discord.ext import commands
from utils.helpers import gera_numero_aleatorio, saudacao

class Diversao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.jogos_forca = {}

        # Listas de conteúdo
        self.frases = [
            "O rato roeu a roupa do rei de Roma.",
            "A rápida raposa marrom pula sobre o cão preguiçoso.",
            "O céu azul reflete as nuvens brancas.",
            "Viver é a coisa mais rara do mundo. A maioria das pessoas existe, isso é tudo.",
            "A persistência é o caminho do êxito."
        ]
        self.piadas = [
            "Por que o livro de matemática se suicidou? Porque estava cheio de problemas.",
            "Qual é o animal mais antigo? A zebra, porque é preta e branca!",
            "Por que o coelho não gosta de contar segredo? Porque ele é muito fofoqueiro!"
        ]
        self.memes = [
            "https://i.pinimg.com/originals/47/55/8f/47558f80001a0d2f85ec053d032c349d.jpg",
            "https://i.pinimg.com/originals/8f/8f/1f/8f8f1f97e34c11c5b13fc9734f4b5864.jpg"
        ]
        self.gifs = [
            "https://media.giphy.com/media/3o7bu2Q3nN3M2cAtla/giphy.gif",
            "https://media.giphy.com/media/8vQSQ3KkV8wzO/giphy.gif"
        ]
        self.palavras_forca = [
            "abacaxi", "programador", "discord", "python", "biscoito", "guitarra", "computador"
        ]

    @commands.command(name="saudacao")
    async def saudacao(self, ctx: commands.Context):
        mensagem = saudacao(ctx.author.name)
        await ctx.send(mensagem)

    @commands.command(name="numero")
    async def gera_numero_aleatorio(self, ctx: commands.Context, minimo: int, maximo: int):
        numero = gera_numero_aleatorio(minimo, maximo)
        await ctx.send(f"O número aleatório gerado é: {numero}")
        await self.dar_xp(ctx)

    @commands.command()
    async def piada(self, ctx: commands.Context):
        await ctx.send(random.choice(self.piadas))
        await self.dar_xp(ctx)

    @commands.command()
    async def meme(self, ctx: commands.Context):
        await ctx.send(random.choice(self.memes))
        await self.dar_xp(ctx)

    @commands.command()
    async def gif(self, ctx: commands.Context):
        await ctx.send(random.choice(self.gifs))
        await self.dar_xp(ctx)

    @commands.command()
    async def forca(self, ctx: commands.Context):
        palavra = random.choice(self.palavras_forca).lower()
        self.jogos_forca[ctx.channel.id] = {
            "palavra": palavra,
            "tentativas": [],
            "chances": 6
        }
        await ctx.send(f"🎮 **Jogo da Forca iniciado!**\nPalavra: {self._mostrar_palavra(palavra, [])}\nVocê tem 6 chances. Use `!chutar <letra>` para jogar.")

    @commands.command()
    async def chutar(self, ctx: commands.Context, letra: str):
        letra = letra.lower()
        jogo = self.jogos_forca.get(ctx.channel.id)

        if not jogo:
            await ctx.send("❌ Nenhum jogo ativo. Use `!forca` para começar.")
            return

        if len(letra) != 1 or not letra.isalpha():
            await ctx.send("❌ Digite apenas uma letra.")
            return

        if letra in jogo["tentativas"]:
            await ctx.send("⚠️ Você já tentou essa letra.")
            return

        jogo["tentativas"].append(letra)

        if letra not in jogo["palavra"]:
            jogo["chances"] -= 1
            await ctx.send(f"❌ Letra incorreta! Chances restantes: {jogo['chances']}")
        else:
            await ctx.send("✅ Letra correta!")

        palavra_mostrada = self._mostrar_palavra(jogo["palavra"], jogo["tentativas"])
        await ctx.send(f"Palavra: {palavra_mostrada}")

        if all(l in jogo["tentativas"] for l in jogo["palavra"]):
            await ctx.send("🎉 Parabéns! Você venceu o jogo da forca!")
            del self.jogos_forca[ctx.channel.id]
        elif jogo["chances"] <= 0:
            await ctx.send(f"💀 Você perdeu! A palavra era **{jogo['palavra']}**.")
            del self.jogos_forca[ctx.channel.id]

        await self.dar_xp(ctx)

    def _mostrar_palavra(self, palavra: str, tentativas: list[str]) -> str:
        return " ".join([letra if letra in tentativas else "_" for letra in palavra])

    @commands.command()
    async def digitar(self, ctx: commands.Context):
        frase = random.choice(self.frases)
        await ctx.send(f"**Desafio de Digitação!**\nDigite a seguinte frase o mais rápido possível:\n\n**{frase}**")

        start_time = time.time()

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)
            end_time = time.time()

            if msg.content.strip() == frase:
                tempo_gasto = round(end_time - start_time, 2)
                xp_ganho = max(10, 30 - int(tempo_gasto))
                await ctx.send(f"Parabéns, {ctx.author.mention}! Você digitou corretamente em {tempo_gasto} segundos e ganhou {xp_ganho} XP!")

                user_id = str(ctx.author.id)
                xp_cog = self.bot.get_cog("XP")
                if xp_cog:
                    xp_cog.add_xp_to_user(user_id, xp=xp_ganho)
            else:
                await ctx.send(f"Você não digitou a frase corretamente, {ctx.author.mention}. Tente novamente!")

        except asyncio.TimeoutError:
            await ctx.send(f"⏱️ Você demorou muito para digitar, {ctx.author.mention}. O tempo acabou!")

    async def dar_xp(self, ctx: commands.Context):
        xp_cog = self.bot.get_cog("XP")
        if xp_cog:
            xp_cog.add_xp_to_user(str(ctx.author.id), min_xp=10, max_xp=25)

async def setup(bot):
    await bot.add_cog(Diversao(bot))

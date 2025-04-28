import random
import discord
from discord.ext import commands
from utils.helpers import gera_numero_aleatorio, saudacao  # Corrigido para importar corretamente a função

class Diversao(commands.Cog):  # Mudado para commands.Cog
    def __init__(self, bot):
        self.bot = bot

    @commands.command()  # Corrigido para usar commands.command()
    async def saudacao(self, ctx):
        """Comando para dar uma saudação ao usuário."""
        mensagem = saudacao(ctx.author.name)  # Usando a função do helpers
        await ctx.send(mensagem)

    @commands.command()
    async def gera_numero_aleatorio(self, ctx, minimo: int, maximo: int):
        """Comando para gerar um número aleatório entre mínimo e máximo."""
        numero = gera_numero_aleatorio(minimo, maximo)  # Usando a função do helpers
        await ctx.send(f"O número aleatório gerado é: {numero}")

    @commands.command()
    async def piada(self, ctx):
        """Comando para enviar uma piada."""
        piadas = [
            "Por que o livro de matemática se suicidou? Porque estava cheio de problemas.",
            "Qual é o animal mais antigo? A zebra, porque é preta e branca!",
            "Por que o coelho não gosta de contar segredo? Porque ele é muito fofoqueiro!"
        ]
        await ctx.send(random.choice(piadas))

    @commands.command()
    async def meme(self, ctx):
        """Comando para enviar um meme (exemplo de um link, pode adicionar mais)"""
        memes = [
            "https://i.pinimg.com/originals/47/55/8f/47558f80001a0d2f85ec053d032c349d.jpg",
            "https://i.pinimg.com/originals/8f/8f/1f/8f8f1f97e34c11c5b13fc9734f4b5864.jpg"
        ]
        await ctx.send(random.choice(memes))

    @commands.command()
    async def gif(self, ctx):
        """Comando para enviar um GIF."""
        gifs = [
            "https://media.giphy.com/media/3o7bu2Q3nN3M2cAtla/giphy.gif",
            "https://media.giphy.com/media/8vQSQ3KkV8wzO/giphy.gif"
        ]
        await ctx.send(random.choice(gifs))

async def setup(bot):
    await bot.add_cog(Diversao(bot))

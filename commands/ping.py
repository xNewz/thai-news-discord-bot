import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        latency = self.bot.latency * 1000  # เป็น ms
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"ความหน่วง: `{latency:.2f} ms`",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))
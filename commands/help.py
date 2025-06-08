# commands/help.py

import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
PREFIX = os.getenv("COMMAND_PREFIX", "/")

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help(self, ctx):
        embed = discord.Embed(
            title="📚 คำสั่งของบอท",
            description="ใช้คำสั่งต่อไปนี้เพื่อใช้งานบอท",
            color=0x008080
        )
        embed.add_field(name=f"`{PREFIX}covid`", value="แสดงสถานการณ์ COVID-19 ในประเทศไทย", inline=True)
        embed.add_field(name=f"`{PREFIX}lotto`", value="แสดงผลสลากกินแบ่งรัฐบาลล่าสุด", inline=True)
        embed.add_field(name=f"`{PREFIX}check_lotto <เลข 6 หลัก>`", value="ตรวจสอบผลรางวัลสำหรับเลขที่ระบุ", inline=True)
        embed.set_footer(text="👨‍💻 พัฒนาโดย Pargorn Ruasijan")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
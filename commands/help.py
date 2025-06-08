# commands/help.py

import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help(self, ctx):
        command_prefix = self.bot.command_prefix if isinstance(self.bot.command_prefix, str) else "/"
        print(command_prefix)
        embed = discord.Embed(
            title="📚 คำสั่งของบอท",
            description="ใช้คำสั่งต่อไปนี้เพื่อใช้งานบอท",
            color=0x008080
        )
        embed.add_field(name=f"`{command_prefix}covid`", value="แสดงสถานการณ์ COVID-19 ในประเทศไทย", inline=True)
        embed.add_field(name=f"`{command_prefix}lotto`", value="แสดงผลสลากกินแบ่งรัฐบาลล่าสุด", inline=True)
        embed.add_field(name=f"`{command_prefix}check_lotto <เลข 6 หลัก>`", value="ตรวจสอบผลรางวัลสำหรับเลขที่ระบุ", inline=True)
        embed.set_footer(text="👨‍💻 พัฒนาโดย Pargorn Ruasijan")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
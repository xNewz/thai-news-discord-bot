# commands/covid.py
import discord
import json
import aiohttp
from discord.ext import commands


class Covid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_data_url(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    @commands.command()
    async def covid(self, ctx):
        try:
            raw = await self.get_data_url(
                "https://disease.sh/v3/covid-19/countries/thailand"
            )
            data = json.loads(raw)

            e = discord.Embed(
                title="สถานการณ์ COVID-19 ในประเทศไทย",
                description="ข้อมูลจาก [disease.sh](https://disease.sh)",
                color=0x008080,
            )

            e.set_thumbnail(url=data["countryInfo"]["flag"])
            e.add_field(
                name="😷 ผู้ป่วยสะสม",
                value=f"{data['cases']:,} (+{data['todayCases']:,})",
                inline=True,
            )
            e.add_field(
                name="✅ หายแล้วสะสม",
                value=f"{data['recovered']:,} (+{data['todayRecovered']:,})",
                inline=True,
            )
            e.add_field(
                name="☠️ เสียชีวิตสะสม",
                value=f"{data['deaths']:,} (+{data['todayDeaths']:,})",
                inline=True,
            )
            e.add_field(name="🧪 ตรวจแล้วทั้งหมด", value=f"{data['tests']:,}", inline=True)
            e.add_field(
                name="📊 ผู้ป่วยที่ยังรักษาอยู่", value=f"{data['active']:,}", inline=True
            )
            e.set_footer(text="👨‍💻 พัฒนาโดย Pargorn Ruasijan")

            await ctx.send(embed=e)
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ เกิดข้อผิดพลาด",
                description=f"{e}",
                color=0xFF0000
            )
            await ctx.send(embed=error_embed)


async def setup(bot):
    await bot.add_cog(Covid(bot))

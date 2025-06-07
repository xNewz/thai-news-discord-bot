import discord
import aiohttp
import json
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} is online")
    await bot.change_presence(activity=discord.Game("/covid"))

async def get_data_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

@bot.command()
async def covid(ctx):
    try:
        raw = await get_data_url('https://disease.sh/v3/covid-19/countries/thailand')
        data = json.loads(raw)

        e = discord.Embed(
            title="สถานการณ์ COVID-19 ในประเทศไทย",
            description="ข้อมูลจาก [disease.sh](https://disease.sh)",
            color=0x008080
        )

        e.set_thumbnail(url=data['countryInfo']['flag'])

        e.add_field(name='😷 ผู้ป่วยสะสม', value=f"{data['cases']:,} (+{data['todayCases']:,})", inline=False)
        e.add_field(name='✅ หายแล้วสะสม', value=f"{data['recovered']:,} (+{data['todayRecovered']:,})", inline=False)
        e.add_field(name='☠️ เสียชีวิตสะสม', value=f"{data['deaths']:,} (+{data['todayDeaths']:,})", inline=False)
        e.add_field(name='🧪 ตรวจแล้วทั้งหมด', value=f"{data['tests']:,}", inline=False)
        e.add_field(name='📊 ผู้ป่วยที่ยังรักษาอยู่', value=f"{data['active']:,}", inline=False)

        e.set_footer(text=f"👨‍💻 พัฒนาโดย Pargorn Ruasijan")

        await ctx.send(embed=e)
    except Exception as e:
        await ctx.send(f"❌ เกิดข้อผิดพลาด: {e}")

bot.run("YOUR_BOT_TOKEN")
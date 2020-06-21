import discord
import aiohttp
import json
from discord.ext import commands

bot = commands.Bot(command_prefix = '/')

@bot.event 
async def on_ready() :
	print(f"{bot.user.name} has started")

@bot.event
async def on_message(message) :
	await bot.process_commands(message)

async def get_data_url(url) :
	async with aiohttp.ClientSession() as session :
		html = await fetch(session, url)

		return html

async def fetch(session, url) :
	async with session.get(url) as respones :
		return await respones.text()

@bot.command()
async def covidth(ctx) :
	thai = await get_data_url('https://covid19.th-stat.com/api/open/timeline')
	thai = json.loads(thai)

	e = discord.Embed(
		title = "รายงานสถานการณ์ โควิด-19 ในประเทศไทย",
		description = f"วันที่ {thai['UpdateDate']}",
		color = 0xFFFF33
	)  

	e.add_field(name='😷 ผู้ป่วยสะสม', value=f"{thai['Data'][-1]['Confirmed']} (เพิ่มขึ้น {thai['Data'][-1]['NewConfirmed']})")
	e.add_field(name='☠ ผู้ป่วยเสียชีวิต', value=f"{thai['Data'][-1]['Deaths']} (เพิ่มขึ่น {thai['Data'][-1]['NewDeaths']})")
	e.add_field(name='🏡 ผู้ป่วยหายแล้ว', value=f"{thai['Data'][-1]['Recovered']} (เพิ่มขึ้น {thai['Data'][-1]['NewRecovered']})")
	e.add_field(name='🏥 รักษาตัวอยู่ รพ.', value=f"{thai['Data'][-1]['Hospitalized']}")

	e.set_footer(text=f'📰 ข้อมูลจาก กรมควมคุมโรค\n👨‍💻 พัฒนาบอทโดย Pargorn Ruasijan')

	await ctx.send(embed=e)

bot.run('#TOKEN HERE')

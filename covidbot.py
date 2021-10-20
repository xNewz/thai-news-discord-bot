import discord
import aiohttp
import json
from discord.ext import commands

bot = commands.Bot(command_prefix = '/')

@bot.event
async def on_ready() :
	print(f"Bot {bot.user.name} has started")
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="/covid_th และ /covid_uthai"))
	
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
async def covid_th(ctx) :
	thai = await get_data_url('https://covid19.ddc.moph.go.th/api/Cases/today-cases-all')
	thai = json.loads(thai)
	print(thai)
	e = discord.Embed(
		title = "รายงานสถานการณ์ โควิด-19 ในประเทศไทย",
		description = f"วันที่ {thai[0]['txn_date']}",
		color = 0xFFFF33
	)

	e.add_field(name='😷 ผู้ป่วยสะสม', value=f"{thai[0]['total_case']} (เพิ่มขึ้น {thai[0]['new_case']})")
	e.add_field(name='☠ ผู้ป่วยเสียชีวิต', value=f"{thai[0]['total_death']} (เพิ่มขึ่น {thai[0]['new_death']})")
	e.add_field(name='🏡 ผู้ป่วยหายแล้ว', value=f"{thai[0]['total_recovered']} (เพิ่มขึ้น {thai[0]['new_recovered']})")

	e.set_footer(text=f'📰 ข้อมูลจาก กรมควมคุมโรค\n👨‍💻 พัฒนาบอทโดย Pargorn Ruasijan')
	await ctx.send(embed=e)

@bot.command()
async def covid_uthai(ctx) :
	thai = await get_data_url('https://covid19.ddc.moph.go.th/api/Cases/today-cases-by-provinces')
	thai = json.loads(thai)
	print(thai[68])
	e = discord.Embed(
		title = "รายงานสถานการณ์ โควิด-19 จังหวัดอุทัยธานี",
		description = f"วันที่ {thai[68]['txn_date']}",
		color = 0x000069
	)

	e.add_field(name='😷 ผู้ป่วยสะสม', value=f"{thai[68]['total_case']} (เพิ่มขึ้น {thai[68]['new_case']})")
	e.add_field(name='☠ ผู้ป่วยเสียชีวิต', value=f"{thai[68]['total_death']} (เพิ่มขึ่น {thai[68]['new_death']})")

	e.set_footer(text=f'📰 ข้อมูลจาก กรมควมคุมโรค\n👨‍💻 พัฒนาบอทโดย Pargorn Ruasijan')
	await ctx.send(embed=e)

bot.run('') #TOKEN HERE

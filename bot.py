import discord
import aiohttp
import json
import os
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} is online")
    await bot.change_presence(activity=discord.Game("/covid, /lotto, /check_lotto"))

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

        e.add_field(name='😷 ผู้ป่วยสะสม', value=f"{data['cases']:,} (+{data['todayCases']:,})", inline=True)
        e.add_field(name='✅ หายแล้วสะสม', value=f"{data['recovered']:,} (+{data['todayRecovered']:,})", inline=True)
        e.add_field(name='☠️ เสียชีวิตสะสม', value=f"{data['deaths']:,} (+{data['todayDeaths']:,})", inline=True)
        e.add_field(name='🧪 ตรวจแล้วทั้งหมด', value=f"{data['tests']:,}", inline=True)
        e.add_field(name='📊 ผู้ป่วยที่ยังรักษาอยู่', value=f"{data['active']:,}", inline=True)

        e.set_footer(text=f"👨‍💻 พัฒนาโดย Pargorn Ruasijan")

        await ctx.send(embed=e)
    except Exception as e:
        await ctx.send(f"❌ เกิดข้อผิดพลาด: {e}")

@bot.command()
async def lotto(ctx):
    try:
        url = "https://lotto.api.rayriffy.com/latest"
        raw = await get_data_url(url)
        data = json.loads(raw)

        if data["status"] != "success":
            await ctx.send("❌ ไม่สามารถโหลดข้อมูลผลสลากได้")
            return

        response = data["response"]
        date = response["date"]
        prizes = response["prizes"]
        running = response["runningNumbers"]

        embed = discord.Embed(
            title=f"🎯 ผลสลากกินแบ่งรัฐบาล งวดวันที่ {date}",
            description="ข้อมูลจาก [lotto.api.rayriffy.com](https://lotto.api.rayriffy.com/swagger)",
            color=0xFF0000
        )

        def find_prize(prize_id):
            return next((p for p in prizes if p["id"] == prize_id), None)

        def find_running(running_id):
            return next((r for r in running if r["id"] == running_id), None)

        # รางวัลที่ 1
        prize_1 = find_prize("prizeFirst")
        if prize_1:
            embed.add_field(
                name=f"🏆 {prize_1['name']} ({int(prize_1['reward']):,})",
                value=", ".join(prize_1["number"]),
                inline=True
            )

        # ข้างเคียงรางวัลที่ 1
        near_1 = find_prize("prizeFirstNear")
        if near_1:
            embed.add_field(
                name=f"🔢 {near_1['name']} ({int(near_1['reward']):,})",
                value=", ".join(near_1["number"]),
                inline=True
            )

        # รางวัลที่ 2
        prize_2 = find_prize("prizeSecond")
        if prize_2:
            embed.add_field(
                name=f"🥈 {prize_2['name']} ({int(prize_2['reward']):,})",
                value=", ".join(prize_2["number"]),
                inline=True
            )

        # รางวัลเลขหน้า 3 ตัว
        front_3 = find_running("runningNumberFrontThree")
        if front_3:
            embed.add_field(
                name=f"🎫 {front_3['name']} ({int(front_3['reward']):,})",
                value=", ".join(front_3["number"]),
                inline=True
            )

        # รางวัลเลขท้าย 3 ตัว
        back_3 = find_running("runningNumberBackThree")
        if back_3:
            embed.add_field(
                name=f"🎫 {back_3['name']} ({int(back_3['reward']):,})",
                value=", ".join(back_3["number"]),
                inline=True
            )

        # รางวัลเลขท้าย 2 ตัว
        back_2 = find_running("runningNumberBackTwo")
        if back_2:
            embed.add_field(
                name=f"🎟️ {back_2['name']} ({int(back_2['reward']):,})",
                value=", ".join(back_2["number"]),
                inline=True
            )

        embed.set_footer(text="👨‍💻 พัฒนาโดย Pargorn Ruasijan")
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ เกิดข้อผิดพลาด: {e}")

@bot.command()
async def check_lotto(ctx, number: str):
    if not number.isdigit() or len(number) != 6:
        await ctx.send("❌ กรุณากรอกเลข 6 หลัก เช่น `/check_lotto 123456`")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get("https://lotto.api.rayriffy.com/latest") as resp:
            if resp.status != 200:
                await ctx.send("❌ ไม่สามารถดึงข้อมูลหวยได้ในขณะนี้")
                return
            data = await resp.json()

    response = data.get("response", {})
    prizes = response.get("prizes", [])
    running = response.get("runningNumbers", [])
    matched = []

    # ตรวจรางวัลหลัก
    for prize in prizes:
        if number in prize["number"]:
            reward = int(prize["reward"])
            matched.append(f"{prize['name']} (฿{reward:,.0f})")

    # ตรวจรางวัลเลขหน้า 3 ตัว
    if number[:3] in running[0]["number"]:
        reward = int(running[0]["reward"])
        matched.append(f"{running[0]['name']} (฿{reward:,.0f})")

    # ตรวจรางวัลเลขท้าย 3 ตัว
    if number[3:] in running[1]["number"]:
        reward = int(running[1]["reward"])
        matched.append(f"{running[1]['name']} (฿{reward:,.0f})")

    # ตรวจรางวัลเลขท้าย 2 ตัว
    if number[-2:] in running[2]["number"]:
        reward = int(running[2]["reward"])
        matched.append(f"{running[2]['name']} (฿{reward:,.0f})")

    embed_color = 0x29AB87 if matched else 0xFF0000
    date_str = response.get('date', 'ไม่พบข้อมูลวันที่')
    embed = discord.Embed(
        title="🎉 ผลการตรวจหวย!",
        description=(
            f"🔢 เลขที่คุณกรอก: **`{number}`**\n"
            f"🗓️ งวดวันที่: **{date_str}**\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        color=embed_color
    )

    if matched:
        embed.add_field(
            name="🏆 ยินดีด้วย! คุณถูกรางวัล",
            value="\n".join(f"🎊 **{m}**" for m in matched),
            inline=False
        )
    else:
        embed.add_field(
            name="😢 ไม่ถูกรางวัล",
            value="ขอให้โชคดีในงวดถัดไปนะครับ 🍀",
            inline=False
        )

    embed.set_footer(text="👨‍💻 พัฒนาโดย Pargorn Ruasijan")
    await ctx.send(embed=embed)

bot.run(TOKEN)
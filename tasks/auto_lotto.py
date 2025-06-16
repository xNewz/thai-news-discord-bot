import discord
import json
import aiohttp
import os
import pytz
from dotenv import load_dotenv
from discord.ext import tasks, commands
from datetime import datetime

load_dotenv()

YOUR_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

class AutoLotto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_lotto.start()

    @tasks.loop(minutes=1)
    async def send_lotto(self):
        now = datetime.now(pytz.timezone("Asia/Bangkok"))

        if now.day in [1, 16] and now.hour == 17 and now.minute == 0:
            channel = self.bot.get_channel(int(YOUR_CHANNEL_ID))
            if not channel:
                print("❌ ไม่พบช่อง Discord")
                return

            try:
                async with aiohttp.ClientSession() as session:
                    headers = {"Authorization": f"Bearer {os.getenv('LOTTO_API_TOKEN', '')}"}
                    async with session.get("https://api.pargorn.com/api/lotto/v1/latest", headers=headers) as resp:
                        raw = await resp.text()

                data = json.loads(raw)
                if data["status"] != "success":
                    await channel.send("❌ ไม่สามารถโหลดข้อมูลผลสลากได้")
                    return

                response = data["data"]
                date = response["date"]
                prizes = response["prizes"]
                running = response["runningNumbers"]

                def find_prize(pid): return next((p for p in prizes if p["id"] == pid), None)
                def find_run(rid): return next((r for r in running if r["id"] == rid), None)

                embed = discord.Embed(
                    title=f"🎯 ผลสลากกินแบ่งรัฐบาล งวดวันที่ {date}",
                    description="ข้อมูลจาก [api.pargorn.com](https://api.pargorn.com)",
                    color=0xFF0000,
                )

                prize_1 = find_prize("prizeFirst")
                if prize_1:
                    embed.add_field(name=f"🏆 {prize_1['name']} ({int(prize_1['reward']):,})", value=", ".join(prize_1["number"]), inline=True)

                near_1 = find_prize("prizeFirstNear")
                if near_1:
                    embed.add_field(name=f"🔢 {near_1['name']} ({int(near_1['reward']):,})", value=", ".join(near_1["number"]), inline=True)

                prize_2 = find_prize("prizeSecond")
                if prize_2:
                    embed.add_field(name=f"🥈 {prize_2['name']} ({int(prize_2['reward']):,})", value=", ".join(prize_2["number"]), inline=True)

                front_3 = find_run("runningNumberFrontThree")
                if front_3:
                    embed.add_field(name=f"🎫 {front_3['name']} ({int(front_3['reward']):,})", value=", ".join(front_3["number"]), inline=True)

                back_3 = find_run("runningNumberBackThree")
                if back_3:
                    embed.add_field(name=f"🎫 {back_3['name']} ({int(back_3['reward']):,})", value=", ".join(back_3["number"]), inline=True)

                back_2 = find_run("runningNumberBackTwo")
                if back_2:
                    embed.add_field(name=f"🎟️ {back_2['name']} ({int(back_2['reward']):,})", value=", ".join(back_2["number"]), inline=True)

                embed.set_footer(text="👨‍💻 พัฒนาโดย Pargorn Ruasijan")

                await channel.send(embed=embed)

            except Exception as e:
                await channel.send(f"❌ เกิดข้อผิดพลาด: {str(e)}")

    @send_lotto.before_loop
    async def before_lotto(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(AutoLotto(bot))
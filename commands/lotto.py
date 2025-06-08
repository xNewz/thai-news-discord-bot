# commands/lotto.py

import discord
import json
import aiohttp
from discord.ext import commands


class Lotto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_data_url(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    @commands.command()
    async def lotto(self, ctx):
        try:
            raw = await self.get_data_url(
                "https://lotto.api.rayriffy.com/latest"
            )
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
                color=0xFF0000,
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
                    inline=True,
                )

            # ข้างเคียงรางวัลที่ 1
            near_1 = find_prize("prizeFirstNear")
            if near_1:
                embed.add_field(
                    name=f"🔢 {near_1['name']} ({int(near_1['reward']):,})",
                    value=", ".join(near_1["number"]),
                    inline=True,
                )

            # รางวัลที่ 2
            prize_2 = find_prize("prizeSecond")
            if prize_2:
                embed.add_field(
                    name=f"🥈 {prize_2['name']} ({int(prize_2['reward']):,})",
                    value=", ".join(prize_2["number"]),
                    inline=True,
                )

            # รางวัลเลขหน้า 3 ตัว
            front_3 = find_running("runningNumberFrontThree")
            if front_3:
                embed.add_field(
                    name=f"🎫 {front_3['name']} ({int(front_3['reward']):,})",
                    value=", ".join(front_3["number"]),
                    inline=True,
                )

            # รางวัลเลขท้าย 3 ตัว
            back_3 = find_running("runningNumberBackThree")
            if back_3:
                embed.add_field(
                    name=f"🎫 {back_3['name']} ({int(back_3['reward']):,})",
                    value=", ".join(back_3["number"]),
                    inline=True,
                )

            # รางวัลเลขท้าย 2 ตัว
            back_2 = find_running("runningNumberBackTwo")
            if back_2:
                embed.add_field(
                    name=f"🎟️ {back_2['name']} ({int(back_2['reward']):,})",
                    value=", ".join(back_2["number"]),
                    inline=True,
                )

            embed.set_footer(text="👨‍💻 พัฒนาโดย Pargorn Ruasijan")
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ เกิดข้อผิดพลาด: {e}")


async def setup(bot):
    await bot.add_cog(Lotto(bot))

# commands/lotto.py

import discord
import json
import aiohttp
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

class Lotto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_data_url(self, url, headers=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.text()

    @commands.command()
    async def lotto(self, ctx):
        try:
            headers = {"Authorization": f"Bearer {os.getenv('LOTTO_API_TOKEN', '')}"}
            raw = await self.get_data_url("https://api.pargorn.com/api/lotto/v1/latest", headers=headers)
            data = json.loads(raw)
            if data["status"] != "success":
                await ctx.send("❌ ไม่สามารถโหลดข้อมูลผลสลากได้")
                return

            response = data["data"]
            date = response["date"]
            prizes = response["prizes"]
            running = response["runningNumbers"]
            embed = discord.Embed(
                title=f"🎯 ผลสลากกินแบ่งรัฐบาล งวดวันที่ {date}",
                description="ข้อมูลจาก [api.pargorn.com](https://api.pargorn.com)",
                color=0xFF0000,
            )

            def find_prize(prize_id):
                return next((p for p in prizes if p["id"] == prize_id), None)

            def find_running(running_id):
                return next((r for r in running if r["id"] == running_id), None)

            # รางวัลที่ 1
            prize_1 = find_prize("firstPrize")
            if prize_1:
                embed.add_field(
                    name=f"🏆 {prize_1['name']} ({int(prize_1['reward']):,})",
                    value=", ".join(prize_1["number"]),
                    inline=True,
                )

            # ข้างเคียงรางวัลที่ 1
            near_1 = find_prize("firstPrizeAdjacent")
            if near_1:
                embed.add_field(
                    name=f"🔢 {near_1['name']} ({int(near_1['reward']):,})",
                    value=", ".join(near_1["number"]),
                    inline=True,
                )

            # รางวัลที่ 2
            prize_2 = find_prize("secondPrize")
            if prize_2:
                embed.add_field(
                    name=f"🥈 {prize_2['name']} ({int(prize_2['reward']):,})",
                    value=", ".join(prize_2["number"]),
                    inline=True,
                )

            # รางวัลเลขหน้า 3 ตัว
            front_3 = find_running("frontThreeDigits")
            if front_3:
                embed.add_field(
                    name=f"🎫 {front_3['name']} ({int(front_3['reward']):,})",
                    value=", ".join(front_3["number"]),
                    inline=True,
                )

            # รางวัลเลขท้าย 3 ตัว
            back_3 = find_running("backThreeDigits")
            if back_3:
                embed.add_field(
                    name=f"🎫 {back_3['name']} ({int(back_3['reward']):,})",
                    value=", ".join(back_3["number"]),
                    inline=True,
                )

            # รางวัลเลขท้าย 2 ตัว
            back_2 = find_running("backTwoDigits")
            if back_2:
                embed.add_field(
                    name=f"🎟️ {back_2['name']} ({int(back_2['reward']):,})",
                    value=", ".join(back_2["number"]),
                    inline=True,
                )

            embed.set_footer(text="👨‍💻 พัฒนาโดย Pargorn Ruasijan")
            try:
                await ctx.send(embed=embed)
            except discord.HTTPException as e:
                await ctx.send(
                    embed=discord.Embed(
                        title="❌ ไม่สามารถส่ง embed ได้",
                        description=f"เกิดข้อผิดพลาด: {e}",
                        color=0xFF0000,
                    )
                )

        except Exception as e:
            await ctx.send(
                embed=discord.Embed(
                    title="❌ เกิดข้อผิดพลาด", description=str(e), color=0xFF0000
                )
            )


async def setup(bot):
    await bot.add_cog(Lotto(bot))

# ใช้ base image ที่มี Python
FROM python:3.11-slim

# ตั้ง working directory
WORKDIR /app

# คัดลอกไฟล์ทั้งหมดไปยัง container
COPY . /app

# ติดตั้ง dependencies ถ้ามี (ปรับตามโค้ดของคุณ)
# หากมี requirements.txt ให้ใช้คำสั่งนี้:
# RUN pip install -r requirements.txt

# หากไม่มี ให้ติดตั้งที่จำเป็นโดยตรง (เช่น discord.py, aiohttp)
RUN pip install discord.py aiohttp

# คำสั่งที่ใช้รัน bot
CMD ["python", "bot.py"]
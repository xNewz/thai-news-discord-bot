FROM python:3.11-slim-bullseye

WORKDIR /app

RUN apt-get update && \
	apt-get install -y --no-install-recommends tzdata && \
	ln -fs /usr/share/zoneinfo/Asia/Bangkok /etc/localtime && \
	dpkg-reconfigure -f noninteractive tzdata && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "bot.py"]
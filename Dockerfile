FROM python:3.11-alpine as base

RUN apk add gcc cmake

RUN pip install --upgrade pip

WORKDIR /app

COPY fake_news_bot /app/fake_news_bot
COPY main.py /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
FROM python:3.11-alpine as base

RUN pip install --upgrade pip

COPY . /app

WORKDIR /app

RUN pip install "langchain[llms]" "google-api-python-client>=2.100.0" python-dotenv python-telegram-bot langchain-google-genai pillow

ENTRYPOINT ["python", "main.py"]
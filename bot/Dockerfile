FROM python:3.11.9

WORKDIR /bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements/requirements_bot.txt /bot/requirements_bot.txt
RUN pip install -r requirements_bot.txt


COPY . .
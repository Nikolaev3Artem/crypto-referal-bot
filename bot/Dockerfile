FROM python:3.11.9-alpine

WORKDIR /bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /bot
RUN pip install -r requirements.txt

COPY . .
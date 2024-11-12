# pull official base image
FROM python:3.11-alpine

# set work directory
WORKDIR /bot

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /bot
RUN pip install -r requirements.txt

# copy project
COPY . .
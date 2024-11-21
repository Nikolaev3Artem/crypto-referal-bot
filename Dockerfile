FROM python:3.11.9

WORKDIR /project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements/requirements_base.txt /project/requirements_base.txt
RUN pip install -r requirements_base.txt

COPY . /project
FROM python:3.11.9-alpine

WORKDIR /project

COPY requirements.txt /project/requirements.txt


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /project

RUN ["chmod", "+x", "/project/entrypoint.sh"]
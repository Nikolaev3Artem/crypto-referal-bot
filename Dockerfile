FROM python:3.11.9

WORKDIR /project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements/requirements_api.txt /project/requirements_api.txt
RUN pip install -r requirements_api.txt

COPY . /project

RUN ["chmod", "+x", "/project/entrypoint.sh"]
FROM python:3.11.9

WORKDIR /project

COPY requirements/requirements_api.txt /project/requirements_api.txt


RUN pip install --upgrade pip
RUN pip install -r requirements_api.txt

COPY . /project

RUN ["chmod", "+x", "/project/entrypoint.sh"]
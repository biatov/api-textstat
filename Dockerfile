FROM python:3.9-slim

WORKDIR /var/app/
COPY . /var/app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONPATH=/var/app
EXPOSE 8080

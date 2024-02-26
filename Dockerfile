FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /convertor

COPY . .

RUN pip install -r requirements.txt
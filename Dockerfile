FROM python:3.7.5-slim

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt requirements.txt


RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 5000
CMD ["python", "./app.py"]

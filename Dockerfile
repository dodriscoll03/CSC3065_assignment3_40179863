FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt requirements.txt


RUN pip install -r requirements.txt

COPY . .

WORKDIR /search_engine

ENTRYPOINT [ "python" ]

CMD ["./main.py"]

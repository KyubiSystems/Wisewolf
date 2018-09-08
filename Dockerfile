FROM python:stretch
MAINTAINER Kyubi Systems 2018

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y build-essential gcc && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python", "./start.py" ]

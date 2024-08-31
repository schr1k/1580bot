FROM python:3.12-alpine

WORKDIR /app

RUN apk update && apk add musl musl-utils musl-locales tzdata

RUN echo 'Europe/Moscow' >  /etc/timezone

RUN echo 'export LC_ALL=ru_RU.UTF-8' >> /etc/profile.d/locale.sh

ENV TZ=Europe/Moscow

ENV LC_ALL ru_RU.UTF-8

ENV LANG ru_RU.UTF-8

ENV LANGUAGE ru_RU.UTF-8

COPY . .

RUN mkdir "logs"

RUN pip install -r requirements.txt

CMD ["python3.11", "-u", "main.py"]

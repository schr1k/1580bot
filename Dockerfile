FROM python:3.12-alpine

ENV MUSL_LOCPATH="/usr/share/i18n/locales/musl"

ENV TZ=Europe/Moscow

ENV LC_ALL ru_RU.UTF-8

ENV LANG ru_RU.UTF-8

ENV LANGUAGE ru_RU.UTF-8

RUN apk update && apk --no-cache add \
    poppler-utils \
    musl-locales \
    musl-utils

RUN echo 'Europe/Moscow' >  /etc/timezone  \
    echo 'export LC_ALL=ru_RU.UTF-8' >> /etc/profile.d/locale.sh

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python3.12", "-u", "main.py"]

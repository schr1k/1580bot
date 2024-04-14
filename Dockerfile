FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN apk update

RUN apk add poppler-utils tzdata

RUN ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime

RUN pip install -r requirements.txt

RUN mkdir "logs"

CMD ["python3.11", "-u", "main.py"]

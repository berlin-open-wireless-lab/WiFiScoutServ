FROM python:3

MAINTAINER Nothyp <nothyp@pcksr.net>

ENV PYTHONUNBUFFERED=1
ENV DJANGO_DEBUG=''
ENV DJANGO_SETTINGS_MODULE=wifidb.settings

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN chmod +x start.sh
RUN pip install -r requirements.txt
RUN python manage.py migrate

EXPOSE 8000

CMD ["sh", "start.sh"]

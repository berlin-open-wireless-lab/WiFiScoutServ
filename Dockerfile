FROM python:3

LABEL maintainer="Pierre Kuhner <pierre@pcksr.net>"

RUN pip install -U pip

ENV PYTHONUNBUFFERED=1 \
    DJANGO_DEBUG='' \
    DJANGO_SETTINGS_MODULE=wifidb.settings

RUN mkdir /app
WORKDIR /app
COPY . /app/

RUN pip install -Ur requirements.txt
RUN curl -o manuf https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf;hb=HEAD

EXPOSE 8000

RUN chmod +x start.sh
CMD ["/app/start.sh"]

# WiFiScoutServ

**WARNING:** currently not suitable for production use!

The API backend for https://github.com/berlin-open-wireless-lab/WiFiSCORE .

A demo is available at https://wifiscout.pcksr.net/

You will also need the following:
- WiFiSCORE (JSON device database): https://github.com/berlin-open-wireless-lab/WiFiSCORE/
- WiFiDePict (picture database): https://github.com/berlin-open-wireless-lab/WiFiDePict/

## Manual installation

These instructions are suitable to test the application with Django built-in development server in debug mode.

### Python dependencies

```
pip install -r requirements.txt
```

A `Pipfile` is included if you are familiar with [`pipenv`](https://github.com/kennethreitz/pipenv).

#### Device pictures

Change the `MEDIA_ROOT` value to the path of your picture database, *e.g*:

```
MEDIA_ROOT = '../WiFiDePict'
```

#### OUI database

You also need a wireshark OUI database file for OUI lookups. The last version is available at https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf;hb=HEAD

Then add its path in your `wifidb/settings.py`:

```
OUI_FILE=manuf
```

### Other settings

```
ADMIN_NAME = "WiFiScout Administration" # The name displayed on the admin interface
AUTH_API_KEY_PARAM = 'key' # The name of the GET parameter for the API key
JSON_DB_PATH = '../WiFiSCORE/' # The path to the JSON database
JSON_DB_FILE_NAME = 'device.json' # The name of device JSON files
```

### Django Setup

```
python manage.py migrate
python manage.py createsuperuser
python dbtool.py --todb <PATH_TO_JSON_DATABASE>
```

### Run

`python manage.py runserver 0.0.0.0:8000`

## Production

**WARNING:** currently not suitable for production use!

### Environment variables

You will need the following environment variables:

- `DJANGO_SECRET_KEY=<SECRET KEY>` the secret key used by Django
- `DJANGO_DEBUG=''` set this variable to anything so that the application run in production mode
- `DJANGO_SETTINGS_MODULE=wifidb.settings`

You can write them in a `.env` file and then `source` it.

To generate a secret key, I use the following Python one-liner:

```
python -c "import string,random; uni=string.ascii_letters+string.digits+string.punctuation; print repr(''.join([random.SystemRandom().choice(uni) for i in range(random.randint(60,65))]))"
```

### Gunicorn

(`<APP_PATH>` is the path to the root directory)

Gunicorn is a Python WSGI HTTP Server used to serve the Django application.

```
gunicorn --workers 3 --bind unix:<APP_PATH>/wifidb.sock
```

To run gunicorn as a daemon service, I use the following systemd unit file:

`/etc/systemd/service/gunicorn.service:`
```
[Unit]
Description=gunicorn daemon
After=network.target
After=nginx.service

[Service]
EnvironmentFile=-<APP_PATH>/.env
User=wifiscout
Group=wifiscout
WorkingDirectory=<APP_PATH>
ExecStart=/usr/bin/gunicorn --workers 3 --bind unix:<APP_PATH>/wifidb.sock wifidb.wsgi:application

[Install]
WantedBy=multi-user.target
```

Then:
```
systemctl start gunicorn
systemctl status gunicorn
```

If everything's OK:
```
systemctl enable gunicorn
```

### Reverse proxy and static files

```
python manage.py collectstatic
```

The following instructions are suitable for using nginx as a reverse proxy.

```
location / {
    proxy_pass         http://unix:<APP_PATH>/wifidb.sock;
    proxy_redirect     off;
    proxy_set_header   Host $host;
    proxy_set_header   X-Real-IP $remote_addr;
    proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header   X-Forwarded-Host $server_name;
}

location /pictures/ {
        alias <PATH_TO_PICTURES_FOLDER>;
        autoindex off;
}

location /static/ {
        alias <APP_PATH>/static/;
        autoindex off;
}
```

## Installation using Docker

A `Dockerfile` is provided.
An automated build is available at https://hub.docker.com/r/pkuhner/wifiscoutserv/

As the process inside Docker does not run as root and still need 
to have read/write permissions on host folders, you need to pass
the ID of your user when running docker run, see below for an example. 

Also, you need to mount the staticfiles, pictures and JSON database folders.

Run the container using the following command:

```
docker run -e LOCAL_USER_ID=`id -u $USER` -v <ABSOLUTE_PATH_TO_WIFISCOUTSERV>/db:/app/db:Z -v <ABSOLUTE_PATH_TO_WIFISCOUTSERV>/static:/app/static:Z -v <PATH_TO_WiFiDePict>:/WiFiDePict:z -v <PATH_TO_WiFiSCORE>:/WiFiSCORE:z  -it -p 8000:8000 --name=wifiscoutserv -d pkuhner/wifiscoutserv
```

This also assumes that your WiFiSCORE and WiFiDePict folders are readable/writable by www-data.

Then, configure your reverse proxy to point to the container. For instance with Nginx:

```
proxy_pass         http://localhost:8000;
```

### Local development using docker-compose

A `docker-compose.yml` file is provided.
To start local version use

    docker-compose up --build

## Usage

You can register at http://localhost:8000/accounts/signup/ and you will be provided with an API key.

- Device list: http://localhost:8000/api/v1/device?key= `<API_KEY>`
- Device details:
    - http://localhost:8000/api/v1/device?key= `<API_KEY>`&signature=`<SIGNATURE>`
    - http://localhost:8000/api/v1/device?key= `<API_KEY>`&signature=`<SIGNATURE>`&oui=`<MAC_VENDOR>`

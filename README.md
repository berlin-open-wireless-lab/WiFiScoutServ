# WiFiScoutServ

**WARNING:** currently not suitable for production use!

The API backend.

You will also need the following:
- WiFiSCORE (JSON device database): https://github.com/berlin-open-wireless-lab/WiFiSCORE/
- WiFiDePict (picture database): https://github.com/berlin-open-wireless-lab/WiFiDePict/

## Manual installation

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

Then add its path in your `settings.py`:

```
OUI_FILE=manuf
```

### Django Setup

```
python manage.py migrate
python manage.py createsuperuser
python dbtool.py --todb <PATH_TO_JSON_DATABASE>
```

### Run

`python manage.py runserver 0.0.0.0:8000`

## Installation using Docker

**Note:** isn't ready yet. Database is in the container, so it's lost if you stop it.

A Dockerfile is provided.

## Usage

You can register at http://localhost:8000/signup and you will be provided with an API key.

- Device list: http://localhost:8000/api/v1/device?key= `<API_KEY>`
- Device details:
    - http://localhost:8000/api/v1/device?key= `<API_KEY>`&id=`<ID>`
    - http://localhost:8000/api/v1/device?key= `<API_KEY>`&sign=`<SIGNATURE>`
    - http://localhost:8000/api/v1/device?key= `<API_KEY>`&sign=`<SIGNATURE>`&oui=`<MAC VENDOR>`

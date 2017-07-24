#!/usr/bin/env python3

import argparse
import json
import os
import sys
from uuid import UUID

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wifidb.settings')
django.setup()

from django.conf import settings

from rest_framework.parsers import JSONParser

from devices.models import Device, Category
from devices.serializers import DeviceSerializer, CategorySerializer

DB_JSON_FILE_NAME = 'device.json'


def is_uuid4(s):
    try:
        val = UUID(s, version=4)
    except ValueError:
        return False

    return True


def get_categories(path):
    categories = []
    dirs = []

    for root, ds, fs in os.walk(path):
        if '.git' in root:
            continue

        root = root.replace(path, '')
        dirs.append(root.strip('/').split('/'))

    for d in dirs:
        if d not in categories and len(d) > 0 and d[0] is not '':
            if not is_uuid4(d[-1]):
                for i, c in enumerate(d):
                    d[i] = c.replace('-', '/')
                categories.append(d)

    return categories


def create_categories(categories):
    qs = Category.objects.all()

    for c in sorted(categories, key=len):
        name = c[-1]
        f = qs.filter(name=name)

        if len(f) == 0:
            parent_id = None
            if len(c) > 1:
                parent = c[-2]
                parent_id = qs.filter(name=parent)[0].id
            try:
                cat_parent = Category.objects.get(id=parent_id)
            except Exception:
                cat_parent = None
            nc = Category(name=name, parent=cat_parent)
            nc.save()


def clean_device(device):
    cat = Category.objects.get(name=device["categories"][0])
    s = CategorySerializer(cat)

    device["category"] = s.data["id"]

    return device


def create_device(device):
    serializer = DeviceSerializer(data=device)
    if serializer.is_valid():
        print(serializer.save())


def update_device(instance, device):
    serializer = DeviceSerializer(instance, data=device)
    if serializer.is_valid():
        print(serializer.save())


def handler_tojson(json_path):
    devices = Device.objects.all()

    for d in devices:
        file_path = json_path + d.get_path()

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        s = DeviceSerializer(d)
        with open(file_path + DB_JSON_FILE_NAME, 'w') as f:
            s.data["image_url"] = s.data["image_url"].replace(settings.MEDIA_URL, '')
            f.write(json.dumps(s.data, indent=4))

    return len(devices)


def handler_todb(json_path):
    n = 0
    categories = get_categories(json_path)

    try:
        create_categories(categories)
    except Exception as e:
        print("ERROR: %s" % (str(e)))

    for root, ds, fs in os.walk(json_path):
        if '.git' in root:
            continue

        if is_uuid4(root.split('/')[-1]):
            fpath = root + '/' + DB_JSON_FILE_NAME
            with open(fpath, 'r') as f:
                data = json.loads(f.read())
                device = clean_device(data)

                try:
                    instance = Device.objects.get(uuid=device["uuid"])
                    update_device(instance, device)
                except Device.DoesNotExist:
                    create_device(device)

                n += 1

    return n


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('json_db', type=str,
                        help='the path to the JSON database')
    mode = parser.add_argument_group("mode")
    exc_mode = mode.add_mutually_exclusive_group()

    exc_mode.add_argument('--todb', action="store_true",
                          help='load JSON data into the Django database')
    exc_mode.add_argument('--tojson', action="store_true",
                          help='dump the Django database')

    n = 0
    args = parser.parse_args()

    if args.json_db[-1] is not '/':
        args.json_db += '/'

    if args.tojson:
        if not os.path.exists(args.json_db):
            print("ERROR: the specified path (%s) does not exist." % (args.json_db))
            sys.exit(-1)

        n = handler_tojson(args.json_db)
    elif args.todb:
        n = handler_todb(args.json_db)
    else:
        print("You must either use --todb or --tojson.")
        sys.exit(-1)

    print("\nDumped/loaded", n, "devices.")


if __name__ == "__main__":
    sys.exit(main())

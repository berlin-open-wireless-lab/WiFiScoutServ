# Generated by Django 2.1.5 on 2019-02-07 16:21

import devices.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_auto_20190206_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='image',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to=devices.models.device_directory_path),
        ),
    ]

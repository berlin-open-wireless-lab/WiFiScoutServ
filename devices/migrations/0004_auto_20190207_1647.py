# Generated by Django 2.1.5 on 2019-02-07 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0003_auto_20190207_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='image_url',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]
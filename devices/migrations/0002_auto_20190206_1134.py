# Generated by Django 2.1.5 on 2019-02-06 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wifi_signature', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['-wifi_signature'],
            },
        ),
        migrations.RemoveField(
            model_name='device',
            name='wifi_signature',
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='child', to='devices.Category'),
        ),
        migrations.AlterField(
            model_name='device',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='devices.Category'),
        ),
        migrations.AddField(
            model_name='device',
            name='signature_24',
            field=models.ManyToManyField(related_name='device_signature_24', to='devices.Signature'),
        ),
        migrations.AddField(
            model_name='device',
            name='signature_5',
            field=models.ManyToManyField(related_name='device_signature_5', to='devices.Signature'),
        ),
    ]

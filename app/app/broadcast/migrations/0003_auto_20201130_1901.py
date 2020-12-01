# Generated by Django 3.1.3 on 2020-12-01 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('broadcast', '0002_auto_20201130_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='broadcastasset',
            name='md5sum',
        ),
        migrations.AddField(
            model_name='broadcastasset',
            name='fingerprint',
            field=models.UUIDField(null=True, unique=True),
        ),
    ]

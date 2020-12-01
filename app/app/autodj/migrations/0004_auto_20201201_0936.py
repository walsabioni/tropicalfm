# Generated by Django 3.1.3 on 2020-12-01 17:36

import common.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodj', '0003_auto_20201130_1901'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rotatorasset',
            options={'ordering': ('title', 'id'), 'verbose_name': 'rotator asset', 'verbose_name_plural': 'rotator assets'},
        ),
        migrations.AddField(
            model_name='audioasset',
            name='album_normalized',
            field=common.models.TruncatingCharField(db_index=True, default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='audioasset',
            name='title_normalized',
            field=common.models.TruncatingCharField(db_index=True, default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='audioasset',
            name='artist_normalized',
            field=common.models.TruncatingCharField(db_index=True, max_length=255),
        ),
    ]

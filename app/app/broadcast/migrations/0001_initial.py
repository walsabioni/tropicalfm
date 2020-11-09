# Generated by Django 3.1.3 on 2020-11-10 02:18

import common.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BroadcastAsset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='last modified')),
                ('title', common.models.TruncatingCharField(blank=True, help_text="If left empty, a title will be generated from the file's metadata.", max_length=255, verbose_name='title')),
                ('file', models.FileField(blank=True, help_text='You can provide either an uploaded audio file or a URL to an external asset.', upload_to=common.models.audio_asset_file_upload_to, verbose_name='audio file')),
                ('duration', models.DurationField(default=datetime.timedelta(0), verbose_name='Audio duration')),
                ('status', models.CharField(choices=[('-', 'upload pending'), ('u', 'uploaded'), ('q', 'download queued'), ('r', 'download running'), ('f', 'download failed')], db_index=True, default='-', max_length=1, verbose_name='upload status')),
                ('task_id', models.UUIDField(null=True)),
                ('uploader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='uploader')),
            ],
            options={
                'verbose_name': 'scheduled broadcast asset',
                'verbose_name_plural': 'scheduled broadcast assets',
            },
        ),
        migrations.CreateModel(
            name='Broadcast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='last modified')),
                ('scheduled_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('-', 'pending'), ('q', 'queued'), ('p', 'played'), ('f', 'queuing failed')], default='-', max_length=1)),
                ('task_id', models.UUIDField(null=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='broadcast.broadcastasset', verbose_name='audio file')),
            ],
            options={
                'verbose_name': 'scheduled broadcast',
                'verbose_name_plural': 'scheduled broadcasts',
                'ordering': ('-scheduled_time',),
            },
        ),
    ]

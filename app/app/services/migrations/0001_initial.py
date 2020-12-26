# Generated by Django 3.1.4 on 2020-12-26 06:44

import common.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('autodj', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpstreamServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(help_text='Unique codename to identify this upstream server.', max_length=20, unique=True, verbose_name='name')),
                ('hostname', models.CharField(help_text='Hostname for the server, eg. example.com', max_length=255, verbose_name='hostname')),
                ('protocol', models.CharField(choices=[('http', 'http'), ('https', 'https (secure)')], default='http', help_text="The protocol for the server, if unsure it's likely http", max_length=5, verbose_name='protocol')),
                ('port', models.PositiveSmallIntegerField(help_text='Port for this server, eg. 8000', verbose_name='port')),
                ('telnet_port', models.PositiveIntegerField()),
                ('username', models.CharField(default='source', max_length=255, verbose_name='username')),
                ('password', models.CharField(max_length=255, verbose_name='password')),
                ('mount', models.CharField(help_text='Mount point for the upstream server, eg. /stream', max_length=255, verbose_name='mount point')),
                ('encoding', models.CharField(choices=[('mp3', 'MP3'), ('fdkaac', 'AAC'), ('vorbis.cbr', 'OGG Vorbis'), ('ffmpeg', 'ffmpeg (custom additional arguments needed)')], default='mp3', max_length=20, verbose_name='encoding format')),
                ('bitrate', models.PositiveSmallIntegerField(blank=True, help_text='Encoding bitrate (kbits), blank for a sane default or ffmpeg.', null=True, verbose_name='bitrate')),
                ('mime', models.CharField(blank=True, help_text='MIME format, ie audio/mpeg, leave blank for Liquidsoap to guess. (Needed for ffmpeg.)', max_length=50, verbose_name='MIME format')),
                ('encoding_args', models.JSONField(blank=True, default=None, help_text='Enter any additional arguments for the encoder here. Advanced use cases only, see the <a href="https://www.liquidsoap.info/doc-1.4.3/encoding_formats.html" target="_blank">Liquidsoap docs here</a> for more info. Leave empty or <code>null</code> for none.', null=True, verbose_name='additional arguments for encoding')),
            ],
            options={
                'ordering': ('id',),
                'unique_together': {('hostname', 'port', 'mount')},
            },
        ),
        migrations.CreateModel(
            name='PlayoutLogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Date')),
                ('event_type', models.CharField(choices=[('track', 'Track'), ('dj', 'Live DJ'), ('general', 'General'), ('source', 'Source Transition')], default='general', max_length=10, verbose_name='Type')),
                ('description', common.models.TruncatingCharField(max_length=500, verbose_name='Entry')),
                ('active_source', common.models.TruncatingCharField(default='N/A', max_length=50, verbose_name='Active Source')),
                ('audio_asset', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autodj.audioasset')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'playout log entry',
                'verbose_name_plural': 'playout logs',
                'ordering': ('-created',),
            },
        ),
    ]

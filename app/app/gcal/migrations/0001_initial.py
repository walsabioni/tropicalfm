# Generated by Django 3.1.4 on 2020-12-23 10:28

from django.conf import settings
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import gcal.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleCalendarShowTimes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='last modified')),
                ('show_times', models.JSONField(decoder=gcal.models.DatetimeRangeListJSONDecoder, default=list, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='_show_times', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Google Calendar shows',
                'verbose_name_plural': 'Google Calendar shows',
                'order_with_respect_to': 'user',
            },
        ),
    ]

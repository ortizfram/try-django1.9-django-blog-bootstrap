# Generated by Django 4.2.4 on 2023-09-01 12:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='publish',
            field=models.DateField(default=datetime.datetime(2023, 9, 1, 12, 46, 37, 269527, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
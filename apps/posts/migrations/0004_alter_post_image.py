# Generated by Django 4.2.4 on 2023-08-30 13:38

import apps.posts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_height_field_post_width_field_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to=apps.posts.models.upload_location, width_field='width_field'),
        ),
    ]

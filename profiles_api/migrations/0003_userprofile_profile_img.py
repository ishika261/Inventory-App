# Generated by Django 3.2.5 on 2021-07-06 10:19

from django.db import migrations, models
import profiles_api.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0002_profilefeeditem'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_img',
            field=models.ImageField(blank=True, null=True, upload_to=profiles_api.models.nameFile),
        ),
    ]

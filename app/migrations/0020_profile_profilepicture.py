# Generated by Django 3.1.5 on 2021-04-26 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_petprofile_adopted'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profilePicture',
            field=models.CharField(default='', max_length=2000),
            preserve_default=False,
        ),
    ]

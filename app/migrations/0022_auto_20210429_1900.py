# Generated by Django 3.1.5 on 2021-04-29 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_activity_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='aadhar',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='license',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='panCard',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='vehicleType',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]

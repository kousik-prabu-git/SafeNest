# Generated by Django 3.1.3 on 2021-03-25 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20210321_2023'),
    ]

    operations = [
        migrations.AddField(
            model_name='petprofile',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
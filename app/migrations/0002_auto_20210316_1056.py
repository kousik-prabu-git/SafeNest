# Generated by Django 3.1.3 on 2021-03-16 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='actionStamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='closeStamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

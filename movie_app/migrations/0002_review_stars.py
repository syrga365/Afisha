# Generated by Django 4.2.10 on 2024-02-22 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='stars',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

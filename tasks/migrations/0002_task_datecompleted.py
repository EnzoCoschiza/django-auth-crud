# Generated by Django 5.0.7 on 2024-07-17 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='dateCompleted',
            field=models.DateTimeField(null=True),
        ),
    ]
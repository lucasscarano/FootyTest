# Generated by Django 5.1.7 on 2025-03-31 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('footballnerds', '0009_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='elo',
            field=models.IntegerField(default=1000),
        ),
    ]

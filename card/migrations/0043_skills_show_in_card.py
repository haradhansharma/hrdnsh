# Generated by Django 3.2.8 on 2021-11-13 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0042_auto_20211113_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='skills',
            name='show_in_card',
            field=models.BooleanField(default=True),
        ),
    ]
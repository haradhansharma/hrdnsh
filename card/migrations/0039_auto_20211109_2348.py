# Generated by Django 3.2.8 on 2021-11-09 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0038_auto_20211109_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='works',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]

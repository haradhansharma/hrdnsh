# Generated by Django 3.2.8 on 2021-11-09 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0037_emailtemplate_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='works',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]

# Generated by Django 3.2.8 on 2021-10-18 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0009_auto_20211018_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendsite',
            name='last_degree',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]

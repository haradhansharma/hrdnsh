# Generated by Django 3.2.8 on 2021-10-25 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0034_alter_serviceinquery_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='works',
            name='work_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]

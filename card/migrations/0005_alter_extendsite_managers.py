# Generated by Django 3.2.8 on 2021-10-17 07:15

import django.contrib.sites.managers
from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0004_alter_extendsite_site'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='extendsite',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('on_site', django.contrib.sites.managers.CurrentSiteManager('site')),
            ],
        ),
    ]
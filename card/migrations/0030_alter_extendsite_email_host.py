# Generated by Django 3.2.8 on 2021-10-23 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0029_auto_20211024_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendsite',
            name='email_host',
            field=models.CharField(max_length=256),
        ),
    ]
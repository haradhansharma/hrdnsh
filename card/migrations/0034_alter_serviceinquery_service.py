# Generated by Django 3.2.8 on 2021-10-24 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0033_serviceinquery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceinquery',
            name='service',
            field=models.ForeignKey(help_text='Select Service name', null=True, on_delete=django.db.models.deletion.SET_NULL, to='card.service'),
        ),
    ]
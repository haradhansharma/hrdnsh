# Generated by Django 3.2.8 on 2021-10-20 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0020_alter_skills_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skills',
            name='area',
            field=models.CharField(choices=[('area1', 'Area1'), ('area2', 'Area2')], max_length=20),
        ),
    ]

# Generated by Django 3.2.8 on 2021-10-17 08:32

from django.db import migrations
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('card', '0006_auto_20211017_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='aviable_for',
            field=taggit_autosuggest.managers.TaggableManager(help_text='Write Comma separated Contract Type eg: remote etc', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Avialable For'),
        ),
        migrations.AlterField(
            model_name='extendsite',
            name='site_meta_tag',
            field=taggit_autosuggest.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Meta Tag'),
        ),
        migrations.AlterField(
            model_name='prcategory',
            name='handy_tools',
            field=taggit_autosuggest.managers.TaggableManager(help_text='Write Comma separated Contract Type eg: remote etc', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Handy Tools'),
        ),
        migrations.AlterField(
            model_name='works',
            name='Tag',
            field=taggit_autosuggest.managers.TaggableManager(help_text='Write Comma separated work Type eg: eCommerce, Knitwears etc', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tag'),
        ),
    ]

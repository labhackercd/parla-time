# Generated by Django 2.0.6 on 2018-06-29 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='author_type',
        ),
    ]
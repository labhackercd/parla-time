# Generated by Django 2.0.6 on 2018-08-28 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_remove_author_author_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='speech',
            name='indexes',
            field=models.TextField(blank=True, null=True),
        ),
    ]

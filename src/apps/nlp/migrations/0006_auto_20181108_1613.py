# Generated by Django 2.1.1 on 2018-11-08 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nlp', '0005_remove_analysis_use_indexes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='algorithm',
            field=models.CharField(choices=[('multigram_bow_with_unigram', 'Multigrams Bag of Words with unigrams'), ('multigram_bow_without_unigram', 'Multigrams Bag of Words without unigrams'), ('decision_tree', 'DecisionTree + Naive Bayes')], max_length=100),
        ),
    ]

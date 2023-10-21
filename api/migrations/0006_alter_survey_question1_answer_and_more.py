# Generated by Django 4.2.6 on 2023-10-21 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_survey_participant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='question1_answer',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')], max_length=70),
        ),
        migrations.AlterField(
            model_name='survey',
            name='question2_answer',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')], max_length=70),
        ),
        migrations.AlterField(
            model_name='survey',
            name='question3_answer',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')], max_length=70),
        ),
    ]

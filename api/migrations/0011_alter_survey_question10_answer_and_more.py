# Generated by Django 4.2.6 on 2023-10-22 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_participant_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='question10_answer',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='survey',
            name='question1_answer',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='survey',
            name='question2_answer',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='survey',
            name='question3_answer',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='survey',
            name='question4_answer',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='survey',
            name='question5_answer',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='survey',
            name='question6_answer',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='survey',
            name='question7_answer',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='survey',
            name='question8_answer',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='survey',
            name='question9_answer',
            field=models.CharField(max_length=150),
        ),
    ]

# Generated by Django 4.2.6 on 2023-10-22 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0009_participant_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="participant",
            name="role",
            field=models.CharField(
                choices=[("parent", "parent"), ("child", "child")], max_length=70
            ),
        ),
    ]

# Generated by Django 4.2.6 on 2024-02-27 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("upload", "0013_alter_assessment_classification_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="assessment_classification",
            name="file_name",
            field=models.CharField(
                default="default_file", max_length=100, verbose_name="文件名"
            ),
        ),
    ]

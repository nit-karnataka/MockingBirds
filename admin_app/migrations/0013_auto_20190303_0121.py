# Generated by Django 2.1.7 on 2019-03-03 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0012_auto_20190302_1946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_model',
            name='frequency',
        ),
        migrations.AddField(
            model_name='and_or_search_model',
            name='frequency',
            field=models.IntegerField(default=1),
        ),
    ]

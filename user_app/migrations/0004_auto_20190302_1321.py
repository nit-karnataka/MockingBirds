# Generated by Django 2.1.7 on 2019-03-02 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0003_auto_20190302_1114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='query_model',
            old_name='reg_no',
            new_name='student_id',
        ),
    ]
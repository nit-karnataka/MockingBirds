# Generated by Django 2.1.7 on 2019-03-02 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0008_student_model_date_of_query'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_model',
            name='date_of_tenure_completion',
            field=models.DateField(auto_now=True),
        ),
    ]

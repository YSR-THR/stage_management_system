# Generated by Django 4.2.13 on 2024-06-20 00:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stage_management_app', '0011_remove_students_gender_remove_students_profile_pic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='students',
            old_name='session_start_year',
            new_name='session',
        ),
        migrations.RemoveField(
            model_name='students',
            name='session_end_year',
        ),
    ]

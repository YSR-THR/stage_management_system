# Generated by Django 4.2.13 on 2024-06-21 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stage_management_app', '0015_remove_staffpreference_student_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staffpreference',
            old_name='internship',
            new_name='internships',
        ),
    ]

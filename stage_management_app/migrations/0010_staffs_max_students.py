# Generated by Django 4.2.13 on 2024-06-19 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stage_management_app', '0009_assignment_created_at_assignment_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffs',
            name='max_students',
            field=models.IntegerField(default=1),
        ),
    ]

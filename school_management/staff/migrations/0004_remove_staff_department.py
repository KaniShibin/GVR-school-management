# Generated by Django 5.1.2 on 2024-10-24 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_alter_staff_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='department',
        ),
    ]

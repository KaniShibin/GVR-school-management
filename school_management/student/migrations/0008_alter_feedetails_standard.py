# Generated by Django 5.1.2 on 2024-10-24 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_alter_feedetails_standard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedetails',
            name='standard',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], max_length=2),
        ),
    ]

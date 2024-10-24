# Generated by Django 5.1.2 on 2024-10-17 15:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0003_feeshistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=150)),
                ('category', models.CharField(choices=[('novel', 'Novel'), ('poem', 'Poem'), ('mystery', 'Mystery'), ('fantasy', 'Fantasy'), ('biography', 'Biography'), ('science_fiction', 'Science Fiction'), ('historical', 'Historical')], max_length=50)),
                ('available', models.CharField(default='instock', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='LibraryRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowed_date', models.DateTimeField(blank=True, null=True)),
                ('lend_date', models.DateTimeField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='librarian.book')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
    ]

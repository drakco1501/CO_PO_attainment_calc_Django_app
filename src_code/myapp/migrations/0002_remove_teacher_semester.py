# Generated by Django 5.2 on 2025-06-10 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='semester',
        ),
    ]

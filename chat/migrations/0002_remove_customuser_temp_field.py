# Generated by Django 5.1.4 on 2025-02-08 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='temp_field',
        ),
    ]

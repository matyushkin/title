# Generated by Django 3.1.12 on 2021-06-13 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['timestamp']},
        ),
    ]

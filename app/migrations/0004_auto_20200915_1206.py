# Generated by Django 3.1 on 2020-09-15 02:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='TicketStatus',
        ),
    ]
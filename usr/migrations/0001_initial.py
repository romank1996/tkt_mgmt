# Generated by Django 3.0.9 on 2020-09-09 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('issue_type', models.CharField(max_length=25)),
                ('description', models.TextField(blank=True, max_length=255)),
                ('finish_date', models.DateField(blank=True, null=True)),
                ('priority', models.CharField(choices=[('urgent', 'Urgent'), ('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], default='medium', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('assigned_to', models.IntegerField(blank=True, null=True)),
                ('assigned_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tickets',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TicketStatus',
            fields=[
                ('ticket_id', models.IntegerField(primary_key=True, serialize=False)),
                ('status_id', models.IntegerField()),
                ('change_time', models.DateTimeField(blank=True, null=True)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'ticket_status',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TicketStatusHistory',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('ticket_id', models.IntegerField(blank=True, null=True)),
                ('status_id', models.IntegerField(blank=True, null=True)),
                ('change_time', models.DateTimeField(blank=True, null=True)),
                ('modified_by', models.IntegerField(blank=True, null=True)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'ticket_status_history',
                'managed': False,
            },
        ),
    ]
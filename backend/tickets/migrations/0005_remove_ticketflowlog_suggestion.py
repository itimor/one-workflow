# Generated by Django 3.0.2 on 2020-04-29 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_ticket_customfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketflowlog',
            name='suggestion',
        ),
    ]

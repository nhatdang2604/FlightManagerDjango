# Generated by Django 4.0.4 on 2022-06-05 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_flight_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='flightdetail',
            name='first_class_ticket_price',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='flightdetail',
            name='second_class_ticket_price',
            field=models.IntegerField(null=True),
        ),
    ]
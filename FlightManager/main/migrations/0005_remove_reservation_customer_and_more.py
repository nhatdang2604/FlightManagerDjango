# Generated by Django 4.0.3 on 2022-05-15 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_transition_aiport_flight_transition_aiports'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='flight',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='price',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='ticket_class',
        ),
        migrations.AddField(
            model_name='reservation',
            name='ticket',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.ticket'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='identity_code',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='phone',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
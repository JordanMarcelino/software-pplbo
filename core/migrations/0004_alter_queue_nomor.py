# Generated by Django 4.1.7 on 2023-04-16 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_queue_nomor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="queue",
            name="nomor",
            field=models.IntegerField(unique=True),
        ),
    ]

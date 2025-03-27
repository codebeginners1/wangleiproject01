# Generated by Django 5.1.3 on 2025-03-18 04:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wlapp", "0003_user_age1"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="age2",
            field=models.IntegerField(db_default=18, verbose_name="年龄"),
        ),
        migrations.AlterField(
            model_name="user",
            name="age",
            field=models.IntegerField(db_default=18, verbose_name="年龄"),
        ),
    ]

# Generated by Django 5.1.3 on 2025-03-18 03:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wlapp", "0002_user_age_alter_user_gender_alter_user_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="age1",
            field=models.IntegerField(default=18, verbose_name="年龄"),
        ),
    ]

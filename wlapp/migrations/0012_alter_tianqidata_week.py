# Generated by Django 5.1.3 on 2025-03-26 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wlapp', '0011_alter_tianqidata_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tianqidata',
            name='week',
            field=models.CharField(blank=True, editable=False, max_length=128, verbose_name='星期'),
        ),
    ]

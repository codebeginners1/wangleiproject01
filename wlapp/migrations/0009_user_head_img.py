# Generated by Django 5.1.3 on 2025-03-24 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wlapp', '0008_orderdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='head_img',
            field=models.ImageField(default='', upload_to='head_img', verbose_name='头像'),
        ),
    ]

# Generated by Django 5.1.3 on 2025-03-23 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wlapp', '0007_visitlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderData',
            fields=[
                ('order_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='订单号')),
                ('product_name', models.CharField(max_length=128, verbose_name='产品名称')),
                ('cost_price', models.IntegerField(verbose_name='成本价')),
                ('sale_price', models.IntegerField(verbose_name='销售价')),
                ('sale_num', models.IntegerField(verbose_name='销售数量')),
                ('product_cost', models.IntegerField(verbose_name='产品成本')),
                ('sale_income', models.IntegerField(verbose_name='销售收入')),
                ('sale_profit', models.IntegerField(verbose_name='销售利润')),
            ],
        ),
    ]

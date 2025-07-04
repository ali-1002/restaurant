# Generated by Django 5.2.3 on 2025-06-23 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_rename_order_time_order_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]

# Generated by Django 4.2.15 on 2024-09-14 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0003_customer_description_order_description_order_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Customer',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='Table',
            new_name='table',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='description',
        ),
        migrations.RemoveField(
            model_name='order',
            name='description',
        ),
        migrations.RemoveField(
            model_name='order',
            name='name',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='description',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='name',
        ),
    ]

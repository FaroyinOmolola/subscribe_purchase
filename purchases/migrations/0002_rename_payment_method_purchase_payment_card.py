# Generated by Django 4.2 on 2023-04-16 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='payment_method',
            new_name='payment_card',
        ),
    ]

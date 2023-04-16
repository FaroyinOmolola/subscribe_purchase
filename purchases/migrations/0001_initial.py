# Generated by Django 4.2 on 2023-04-14 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentCard',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('authorization_code', models.CharField(unique=True)),
                ('exp_month', models.CharField()),
                ('exp_year', models.CharField()),
                ('payment_email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('frequency', models.CharField(choices=[('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly'), ('daily', 'Daily'), ('hourly', 'Hourly'), ('minutely', 'Minutely')], max_length=10)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('last_payment_date', models.DateTimeField(blank=True, null=True)),
                ('next_payment_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('stop_deduction', models.BooleanField(blank=True, default=False)),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='purchases.paymentcard')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='purchases.purchase')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
# Generated by Django 5.1.2 on 2024-11-04 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('amount', models.IntegerField()),
                ('order_id', models.CharField(blank=True, max_length=30)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=30)),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
    ]

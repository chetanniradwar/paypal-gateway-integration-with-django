# Generated by Django 3.2.2 on 2021-05-16 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PaymentGatewayIntegration', '0002_auto_20210516_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='capture_id',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]
